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
from supercivilian.core.serializers import ErrorWithMessageSerializer
from supercivilian.core.utilities import success_response_serializer

from .serializers import ShelterSerializer, ShelterSerializerWithDistance
from .utilities import get_details_for_shelter, get_shelters_for_point


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
                    name="ShelterListPayload",
                    serializer=ShelterSerializerWithDistance,
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
            longitude = parameters.float("longitude", required=True)
            latitude = parameters.float("latitude", required=True)
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


class GetShelterDetailsView(views.APIView):
    """GET details for a shelter."""

    @extend_schema(
        operation_id="get_shelter_details",
        tags=["arcgis"],
        summary="Get details for a shelter",
        description="Get details for a shelter",
        responses={
            status.HTTP_200_OK: OpenApiResponse(
                response=success_response_serializer(
                    name="ShelterDetailsPayload",
                    serializer=ShelterSerializer,
                ),
                description="Details for the shelter",
            ),
            status.HTTP_404_NOT_FOUND: OpenApiResponse(
                response=ErrorWithMessageSerializer,
                description="Shelter not found",
            ),
        },
        auth=[],
    )
    def get(self, request: HttpRequest, id: int) -> APIResponse:
        shelter = get_details_for_shelter(id)

        if shelter is None:
            return APIErrorResponse(
                message="Shelter not found", status=status.HTTP_404_NOT_FOUND
            )

        return APISuccessResponse(payload=shelter.dict())
