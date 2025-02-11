from django.http import HttpRequest
from rest_framework.views import APIView

from supercivilian.core.dataclasses import Point
from supercivilian.core.params import ParameterError, SearchParameters
from supercivilian.core.responses import (
    APIErrorResponse,
    APIResponse,
    APISuccessResponse,
)

from .utilities import get_shelters_for_point


class GetSheltersForPointView(APIView):
    """GET shelters within a given range of a point.

    Expects a `longitude` and `latitude` url parameter that contains the point
    coordinates.

    Additionally, the following optional url parameters are supported:
    - `offset`: The offset of the shelters to return. Defaults to 0.
    - `limit`: The number of shelters to return. Defaults to 10.
    - `range`: The range of the shelters to return (in meters). Defaults to
      30km. Can be at most 1000km.

    Responses:
        - 200: A list of shelters.
            - payload: A list of `Shelter` objects, with the `distance`
              attribute set to the distance of the shelter from the point in
              meters. See the `supercivilian.arcgis.dataclasses.Shelter`
              documentation for more information about the `Shelter` object.
        - 400: Invalid query parameters.
        - 500: Internal server error.
    """

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

        point = Point(longitude=longitude, latitude=latitude)

        if range_ > 1000 * 1000:
            return APIErrorResponse(
                message="Range must be less than 1000km", status=400
            )

        shelters = get_shelters_for_point(point, range_, offset, limit)

        return APISuccessResponse(
            payload=([shelter.dict(point) for shelter in shelters] if shelters else [])
        )
