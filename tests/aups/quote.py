import unittest
from tests.aups.fixture import proxy
from gds_helpers import jsonify


class TestAustraliaPostQuote(unittest.TestCase):
    def test_parse_quote_response(self):
        parsed_response = proxy.mapper.parse_quote_response(SHIPPING_PRICE_RESPONSE)
        self.assertEqual(
            jsonify(parsed_response), jsonify(PARSED_SHIPPING_PRICE_RESPONSE)
        )

    def test_parse_quote_response_errors(self):
        parsed_response = proxy.mapper.parse_quote_response(ERRORS)
        self.assertEqual(jsonify(parsed_response), jsonify(PARSED_ERRORS))


PARSED_SHIPPING_PRICE_RESPONSE = [
    [
        {
            "base_charge": 58.74,
            "carrier": "AustraliaPost",
            "currency": "AUD",
            "delivery_date": None,
            "discount": None,
            "duties_and_taxes": 5.87,
            "extra_charges": [{"amount": 4.51, "currency": None, "name": "Fuel"}],
            "service_name": None,
            "service_type": None,
            "total_charge": 64.61,
        }
    ],
    [],
]

PARSED_ERRORS = [
    [],
    [
        {
            "carrier": "AustraliaPost",
            "code": "44003",
            "message": "The product T28S specified in an item has indicated that dangerous goods will be included in the parcel, however, the product does not allow dangerous goods to be sent using the service.  Please choose a product that allows dangerous goods to be included within the parcel to be sent.",
        }
    ],
]


SHIPPING_PRICE_RESPONSE = {
    "shipments": [
        {
            "shipment_reference": "XYZ-001-01",
            "email_tracking_enabled": True,
            "from": {
                "type": "MERCHANT_LOCATION",
                "lines": ["1 Main Street"],
                "suburb": "MELBOURNE",
                "postcode": "3000",
                "state": "VIC",
                "name": "John Citizen",
                "country": "AU",
                "email": "john.citizen@citizen.com",
                "phone": "0401234567",
            },
            "to": {
                "lines": ["123 Centre Road"],
                "suburb": "Sydney",
                "postcode": "2000",
                "state": "NSW",
                "name": "Jane Smith",
                "business_name": "Smith Pty Ltd",
                "country": "AU",
                "email": "jane.smith@smith.com",
                "phone": "0412345678",
            },
            "items": [
                {"weight": 1, "height": 10, "length": 10, "width": 10},
                {"weight": 1, "height": 10, "length": 10, "width": 10},
                {"weight": 1, "height": 10, "length": 10, "width": 10},
            ],
            "shipment_summary": {
                "total_cost": 64.61,
                "total_cost_ex_gst": 58.74,
                "freight_charge": 45.98,
                "transit_cover": 8.25,
                "fuel_surcharge": 4.51,
                "total_gst": 5.87,
                "tracking_summary": {},
                "number_of_items": 4,
            }
        }
    ]
}

SHIPPING_PRICE_REQUEST = {
    "shipments": [
        {
            "shipment_reference": "XYZ-001-01",
            "customer_reference_1": "Order 001",
            "customer_reference_2": "SKU-1, SKU-2, SKU-3",
            "email_tracking_enabled": True,
            "from": {
                "name": "John Citizen",
                "lines": ["1 Main Street"],
                "suburb": "MELBOURNE",
                "state": "VIC",
                "postcode": "3000",
                "phone": "0401234567",
                "email": "john.citizen@citizen.com",
            },
            "to": {
                "name": "Jane Smith",
                "business_name": "Smith Pty Ltd",
                "lines": ["123 Centre Road"],
                "suburb": "Sydney",
                "state": "NSW",
                "postcode": "2000",
                "phone": "0412345678",
                "email": "jane.smith@smith.com",
            },
            "items": [
                {
                    "item_reference": "SKU-1",
                    "product_id": "T28S",
                    "length": "10",
                    "height": "10",
                    "width": "10",
                    "weight": "1",
                    "authority_to_leave": False,
                    "allow_partial_delivery": True,
                    "features": {
                        "TRANSIT_COVER": {"attributes": {"cover_amount": 1000}}
                    },
                },
                {
                    "item_reference": "SKU-2",
                    "product_id": "T28S",
                    "length": "10",
                    "height": "10",
                    "width": "10",
                    "weight": "1",
                    "authority_to_leave": False,
                    "allow_partial_delivery": True,
                },
                {
                    "item_reference": "SKU-3",
                    "product_id": "T28S",
                    "length": "10",
                    "height": "10",
                    "width": "10",
                    "weight": "1",
                    "authority_to_leave": False,
                    "allow_partial_delivery": True,
                },
            ],
        }
    ]
}

ERRORS = {
    "errors": [
        {
            "code": "44003",
            "name": "DANGEROUS_GOODS_NOT_SUPPORTED_BY_PRODUCT_ERROR",
            "message": "The product T28S specified in an item has indicated that dangerous goods will be included in the parcel, however, the product does not allow dangerous goods to be sent using the service.  Please choose a product that allows dangerous goods to be included within the parcel to be sent.",
        }
    ]
}
