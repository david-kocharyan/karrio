from typing import List, Tuple
from purplship.freight.mappers.fedex.settings import Settings
from purplship.freight.mapper import Mapper as BaseMapper
from pyfedex.track_service_v18 import TrackRequest
from pyfedex.ship_service_v25 import ProcessShipmentRequest
from pyfedex.rate_service_v26 import RateRequest as FedexRateRequest
from purplship.core.utils.serializable import Serializable, Deserializable
from purplship.core.models import (
    RateDetails, RateRequest, TrackingDetails, TrackingRequest,
    ShipmentRequest, ShipmentDetails, Error
)
from purplship.carriers.fedex import track_request, parse_track_response
from purplship.carriers.fedex.package import (
    rate_request, parse_rate_response,
    process_shipment_request, parse_shipment_response
)


class Mapper(BaseMapper):
    settings: Settings

    """Request Mappers"""

    def create_rate_request(self, payload: RateRequest) -> Serializable[FedexRateRequest]:
        return rate_request(payload, self.settings)

    def create_tracking_request(self, payload: TrackingRequest) -> Serializable[TrackRequest]:
        return track_request(payload, self.settings)

    def create_shipment_request(self, payload: ShipmentRequest) -> Serializable[ProcessShipmentRequest]:
        return process_shipment_request(payload, self.settings)

    """Response Parsers"""

    def parse_rate_response(self, response: Deserializable[str]) -> Tuple[List[RateDetails], List[Error]]:
        return parse_rate_response(response.deserialize(), self.settings)

    def parse_tracking_response(self, response: Deserializable[str]) -> Tuple[List[TrackingDetails], List[Error]]:
        return parse_track_response(response.deserialize(), self.settings)

    def parse_shipment_response(self, response: Deserializable[str]) -> Tuple[ShipmentDetails, List[Error]]:
        return parse_shipment_response(response.deserialize(), self.settings)
