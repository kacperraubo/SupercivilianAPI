from django.http import HttpRequest
from drf_spectacular.utils import OpenApiParameter, OpenApiResponse, extend_schema
from rest_framework import status, views

from supercivilian.core.dataclasses import Point
from supercivilian.core.params import ParameterError, SearchParameters
from supercivilian.core.responses import (
    APIErrorResponse,
    APIResponse,
    APISuccessResponse,
)
from supercivilian.core.utilities import (
    success_response_serializer,
)
from supercivilian.core.serializers import ErrorWithMessageSerializer

from .serializers import ShelterSerializer
from .utilities import get_shelters_for_point


class GetSheltersForPointView(views.APIView):
    """GET shelters within a given range of a point."""

    @extend_schema(
        operation_id="get_shelters_for_point",
        tags=["arcgis"],
        summary="Get shelters within a given range of a point",
        description="Get shelters within a given range of a point",
        parameters=[
            OpenApiParameter(
                name="longitude",
                description="The longitude of the point",
                required=True,
                type=float,
            ),
            OpenApiParameter(
                name="latitude",
                description="The latitude of the point",
                required=True,
                type=float,
            ),
            OpenApiParameter(
                name="offset",
                description="The offset of the shelters to return",
                default=0,
                type=int,
            ),
            OpenApiParameter(
                name="limit",
                description="The number of shelters to return",
                default=10,
                type=int,
            ),
            OpenApiParameter(
                name="range",
                description="How far from the point to search for shelters (in meters). Maximum is `1000 * 1000`.",
                default=30 * 1000,
                type=int,
            ),
        ],
        responses={
            status.HTTP_200_OK: OpenApiResponse(
                response=success_response_serializer(
                    name="Shelter List",
                    serializer=ShelterSerializer,
                    many=True,
                ),
                description="A list of shelters",
            ),
            status.HTTP_400_BAD_REQUEST: OpenApiResponse(
                response=ErrorWithMessageSerializer,
                description="Invalid query parameters",
            ),
        },
        auth=[],
    )
    def get(self, request: HttpRequest) -> APIResponse:
        parameters = SearchParameters(request)

        try:
            longitude = parameters.string("longitude", required=True)
            latitude = parameters.string("latitude", required=True)
            offset = parameters.integer("offset", default=0)
            limit = parameters.integer("limit", default=10)
            range_ = parameters.integer("range", default=30 * 1000)
        except ParameterError as exception:
            return APIErrorResponse(
                message=str(exception), status=status.HTTP_400_BAD_REQUEST
            )

        point = Point(longitude=longitude, latitude=latitude)

        if range_ > 1000 * 1000:
            return APIErrorResponse(
                message="Range must be less than 1000km",
                status=status.HTTP_400_BAD_REQUEST,
            )

        shelters = get_shelters_for_point(point, range_, offset, limit)

        return APISuccessResponse(
            payload=([shelter.dict(point) for shelter in shelters] if shelters else [])
        )
