from typing import Tuple, List, Any
from pycanadapost.ncshipment import (
    NonContractShipmentType,
    NonContractShipmentInfoType,
    DeliverySpecType,
    SenderType,
    DomesticAddressDetailsType,
    DestinationType,
    DestinationAddressDetailsType,
    ParcelCharacteristicsType,
    optionsType,
    ReferencesType,
    NotificationType,
    sku_listType,
    SkuType,
    dimensionsType,
    OptionType,
    CustomsType,
    PreferencesType,
)
from purplship.core.units import Currency, WeightUnit, Options, Packages
from purplship.core.utils import export, concat_str, Serializable, Element, no_space
from purplship.core.models import (
    Message,
    ShipmentDetails,
    ShipmentRequest,
)
from purplship.providers.canadapost.error import parse_error_response
from purplship.providers.canadapost.units import (
    OptionCode,
    ServiceType,
    PackagePresets,
    INTERNATIONAL_NON_DELIVERY_OPTION
)
from purplship.providers.canadapost.utils import Settings


def parse_shipment_response(
    response: Element, settings: Settings
) -> Tuple[ShipmentDetails, List[Message]]:
    shipment = (
        _extract_shipment(response, settings)
        if len(response.xpath(".//*[local-name() = $name]", name="shipment-id")) > 0
        else None
    )
    return shipment, parse_error_response(response, settings)


def _extract_shipment(response: Element, settings: Settings) -> ShipmentDetails:
    info_node = next(
        iter(response.xpath(".//*[local-name() = $name]", name="shipment-info"))
    )
    label = next(iter(response.xpath(".//*[local-name() = $name]", name="label")))
    errors = parse_error_response(label, settings)
    info: NonContractShipmentInfoType = NonContractShipmentInfoType()
    info.build(info_node)

    return ShipmentDetails(
        carrier_name=settings.carrier_name,
        carrier_id=settings.carrier_id,
        tracking_number=info.tracking_pin,
        shipment_identifier=info.tracking_pin,
        label=label.text if len(errors) == 0 else None,
    )


def shipment_request(payload: ShipmentRequest, _) -> Serializable[NonContractShipmentType]:
    package = Packages(payload.parcels, PackagePresets, required=["weight"]).single
    service = ServiceType[payload.service].value
    options = Options(payload.options, OptionCode)
    is_intl = (
        payload.recipient.country_code is not None and
        payload.recipient.country_code != 'CA'
    )

    def compute_amount(code: str, _: Any):
        if code == OptionCode.insurance.value:
            return options.insurance
        if code == OptionCode.cash_on_delivery.value:
            return options.cash_on_delivery
        return None

    special_services = {
        OptionCode[name].value: compute_amount(OptionCode[name].value, value)
        for name, value in options
    }

    if is_intl and not any(key in special_services for key in INTERNATIONAL_NON_DELIVERY_OPTION):
        special_services['canadapost_return_to_sender'] = OptionCode.canadapost_return_to_sender.value

    request = NonContractShipmentType(
        requested_shipping_point=None,
        delivery_spec=DeliverySpecType(
            service_code=service,
            sender=SenderType(
                name=payload.shipper.person_name,
                company=payload.shipper.company_name,
                contact_phone=payload.shipper.phone_number,
                address_details=DomesticAddressDetailsType(
                    address_line_1=concat_str(payload.shipper.address_line1, join=True),
                    address_line_2=concat_str(payload.shipper.address_line2, join=True),
                    city=payload.shipper.city,
                    prov_state=payload.shipper.state_code,
                    postal_zip_code=no_space(payload.shipper.postal_code),
                ),
            ),
            destination=DestinationType(
                name=payload.recipient.person_name,
                company=payload.recipient.company_name,
                additional_address_info=None,
                client_voice_number=payload.recipient.phone_number,
                address_details=DestinationAddressDetailsType(
                    address_line_1=concat_str(
                        payload.recipient.address_line1, join=True
                    ),
                    address_line_2=concat_str(
                        payload.recipient.address_line2, join=True
                    ),
                    city=payload.recipient.city,
                    prov_state=payload.recipient.state_code,
                    country_code=payload.recipient.country_code,
                    postal_zip_code=no_space(payload.recipient.postal_code),
                ),
            ),
            options=(
                optionsType(
                    option=[
                        OptionType(
                            option_code=code,
                            option_amount=amount,
                            option_qualifier_1=None,
                            option_qualifier_2=None,
                        )
                        for code, amount in special_services.items()
                    ]
                )
                if len(special_services) > 0 else None
            ),
            parcel_characteristics=ParcelCharacteristicsType(
                weight=package.weight.KG,
                dimensions=dimensionsType(
                    length=package.length.CM,
                    width=package.width.CM,
                    height=package.height.CM,
                ),
                unpackaged=None,
                mailing_tube=None,
            ),
            notification=(
                NotificationType(
                    email=options.notification_email or payload.recipient.email,
                    on_shipment=True,
                    on_exception=True,
                    on_delivery=True,
                )
                if options.notification_email is not None else None
            ),
            preferences=PreferencesType(
                show_packing_instructions=True,
                show_postage_rate=True,
                show_insured_value=("insurance" in payload.options),
            ),
            references=ReferencesType(
                cost_centre=None,
                customer_ref_1=payload.reference,
                customer_ref_2=None,
            ),
            customs=(
                CustomsType(
                    currency=Currency.AUD.value,
                    conversion_from_cad=None,
                    reason_for_export=payload.customs.incoterm,
                    other_reason=payload.customs.content_description,
                    duties_and_taxes_prepaid=payload.customs.duty.account_number,
                    certificate_number=None,
                    licence_number=None,
                    invoice_number=None,
                    sku_list=sku_listType(
                        item=[
                            SkuType(
                                customs_number_of_units=item.quantity,
                                customs_description=item.description,
                                sku=item.sku,
                                hs_tariff_code=None,
                                unit_weight=WeightUnit.KG.value,
                                customs_value_per_unit=item.value_amount,
                                customs_unit_of_measure=None,
                                country_of_origin=payload.shipper.country_code,
                                province_of_origin=None,
                            )
                            for item in payload.customs.commodities
                        ]
                    ),
                )
                if payload.customs is not None else None
            ),
            settlement_info=None,
        ),
    )
    return Serializable(request, _request_serializer)


def _request_serializer(request: NonContractShipmentType) -> str:
    return export(
        request,
        name_="non-contract-shipment",
        namespacedef_='xmlns="http://www.canadapost.ca/ws/ncshipment-v4"',
    )
