import dataclasses
from django.http import HttpRequest
from django.views import View

from supercivilian.core.responses import (
    APIErrorResponse,
    APIResponse,
    APISuccessResponse,
)
from supercivilian.core.params import SearchParameters, ParameterError

from .utilities import get_shelters_for_point


class GetSheltersForPointView(View):
    """View for getting shelters for a point."""

    def get(self, request: HttpRequest) -> APIResponse:
        parameters = SearchParameters(request)

        try:
            longitude = parameters.string("longitude", required=True)
            latitude = parameters.string("latitude", required=True)
            offset = parameters.integer("offset", default=0)
            limit = parameters.integer("limit", default=10)
            range_ = parameters.integer("range", default=30 * 1000)
        except ParameterError as exception:
            return APIErrorResponse(message=str(exception), status=400)

        if range_ > 1000 * 100:
            return APIErrorResponse(message="Range must be less than 100km", status=400)

        shelters = get_shelters_for_point(longitude, latitude, range_, offset, limit)

        return APISuccessResponse(
            payload=(
                [dataclasses.asdict(shelter) for shelter in shelters]
                if shelters
                else []
            )
        )
