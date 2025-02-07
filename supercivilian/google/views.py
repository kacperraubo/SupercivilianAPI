from django.views import View
from django.http import HttpRequest

import requests

from supercivilian.core.responses import (
    APIResponse,
    APIErrorResponse,
    APISuccessResponse,
)
from supercivilian.core.params import SearchParameters, ParameterError

from .utilities import generate_places_api_url


class SearchAutoCompleteView(View):
    """Proxy view for the Google Places API autocomplete endpoint."""

    def get(self, request: HttpRequest) -> APIResponse:
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
            return APIErrorResponse(status=404)

        if response.status_code != 200 or status != "OK":
            return APIErrorResponse(status=500)

        return APISuccessResponse(payload=payload.get("predictions"))


class PlaceDetailsView(View):
    """Proxy view for the Google Places API details endpoint."""

    def get(self, request: HttpRequest, id: str) -> APIResponse:
        url = generate_places_api_url(
            "/details/json",
            place_id=id,
            language="pl",
        )

        response = requests.get(url)
        payload = response.json()
        status = payload.get("status")

        if status == "ZERO_RESULTS" or status == "NOT_FOUND":
            return APIErrorResponse(status=404)

        if response.status_code != 200 or status != "OK":
            return APIErrorResponse(status=500)

        return APISuccessResponse(payload=payload.get("result"))
