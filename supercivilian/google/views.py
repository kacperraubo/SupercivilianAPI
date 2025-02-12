import dataclasses

import requests
from drf_spectacular.utils import OpenApiParameter, OpenApiResponse, extend_schema
from rest_framework import status, views
from rest_framework.request import Request

from supercivilian.core.params import ParameterError, SearchParameters
from supercivilian.core.responses import (
    APIErrorResponse,
    APIResponse,
    APISuccessResponse,
)
from supercivilian.core.serializers import ErrorWithMessageSerializer
from supercivilian.core.utilities import success_response_serializer

from .dataclasses import AutocompletePrediction, PlaceDetails
from .serializers import AutocompletePredictionSerializer, PlaceDetailsSerializer
from .utilities import generate_places_api_url


class SearchAutoCompleteView(views.APIView):
    """GET a list of places matching the query in Poland.

    Note the prediction details are returned in Polish.
    """

    @extend_schema(
        operation_id="google_search_autocomplete",
        summary="Search for places by query",
        description="Search for places by query in Poland.",
        parameters=[
            OpenApiParameter(
                name="query",
                description="The query to search for",
                required=True,
                type=str,
            )
        ],
        responses={
            status.HTTP_200_OK: OpenApiResponse(
                response=success_response_serializer(
                    name="Search Auto Complete",
                    serializer=AutocompletePredictionSerializer,
                    many=True,
                ),
                description="A list of predictions for the query",
            ),
            status.HTTP_400_BAD_REQUEST: OpenApiResponse(
                response=ErrorWithMessageSerializer,
                description="Invalid query",
            ),
            status.HTTP_404_NOT_FOUND: OpenApiResponse(
                response=ErrorWithMessageSerializer,
                description="No results found",
            ),
            status.HTTP_500_INTERNAL_SERVER_ERROR: OpenApiResponse(
                response=ErrorWithMessageSerializer,
                description="Internal server error",
            ),
        },
        auth=[],
    )
    def get(self, request: Request) -> APIResponse:
        parameters = SearchParameters(request)

        try:
            query = parameters.string("query", required=True)
        except ParameterError as exception:
            return APIErrorResponse(message=str(exception), status=400)

        url = generate_places_api_url(
            "/autocomplete/json",
            input=query,
            language="pl",
            components="country:pl",
        )

        response = requests.get(url)
        payload = response.json()
        status = payload.get("status")

        if status == "ZERO_RESULTS":
            return APIErrorResponse(message="No results found", status=404)

        if response.status_code != 200 or status != "OK":
            return APIErrorResponse(message="Internal server error", status=500)

        predictions = [
            dataclasses.asdict(
                AutocompletePrediction(
                    place_id=prediction.get("place_id"),
                    description=prediction.get("description"),
                    types=prediction.get("types"),
                )
            )
            for prediction in payload.get("predictions")
        ]

        return APISuccessResponse(payload=predictions)


class PlaceDetailsView(views.APIView):
    """GET details for a place.

    Note the details are returned in Polish.
    """

    @extend_schema(
        operation_id="google_place_details",
        summary="Get details for a place",
        description="Get details for a place.",
        responses={
            status.HTTP_200_OK: OpenApiResponse(
                response=success_response_serializer(
                    name="Place Details",
                    serializer=PlaceDetailsSerializer,
                ),
                description="Details for the place",
            ),
            status.HTTP_404_NOT_FOUND: OpenApiResponse(
                response=ErrorWithMessageSerializer,
                description="Place not found",
            ),
            status.HTTP_500_INTERNAL_SERVER_ERROR: OpenApiResponse(
                response=ErrorWithMessageSerializer,
                description="Internal server error",
            ),
        },
        auth=[],
    )
    def get(self, request: Request, id: str) -> APIResponse:
        url = generate_places_api_url(
            "/details/json",
            place_id=id,
            language="pl",
        )

        response = requests.get(url)
        payload = response.json()
        status = payload.get("status")

        if status == "ZERO_RESULTS" or status == "NOT_FOUND":
            return APIErrorResponse(message="Place not found", status=404)

        if response.status_code != 200 or status != "OK":
            return APIErrorResponse(message="Internal server error", status=500)

        result = dataclasses.asdict(
            PlaceDetails(
                id=payload.get("result").get("place_id"),
                name=payload.get("result").get("name"),
                url=payload.get("result").get("url"),
                formatted_address=payload.get("result").get("formatted_address"),
                website=payload.get("result").get("website"),
            )
        )

        return APISuccessResponse(payload=result)
