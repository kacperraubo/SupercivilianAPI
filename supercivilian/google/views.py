import requests
from rest_framework.request import Request
from rest_framework.views import APIView

from supercivilian.core.params import ParameterError, SearchParameters
from supercivilian.core.responses import (
    APIErrorResponse,
    APIResponse,
    APISuccessResponse,
)

from .utilities import generate_places_api_url


class SearchAutoCompleteView(APIView):
    """GET a list of places matching the query in Poland.

    Expects a `query` url parameter that contains the search query.

    Note the prediction details are returned in Polish.

    Responses:
        - 200: A list of places matching the query.
            - payload: A list of predictions. See [here](https://developers.google.com/maps/documentation/places/web-service/autocomplete#place_autocomplete_responses)
              for more information about the format of a prediction.
        - 400: Invalid query parameter.
        - 404: No places found.
        - 500: Internal server error.
    """

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
            return APIErrorResponse(status=404)

        if response.status_code != 200 or status != "OK":
            return APIErrorResponse(status=500)

        return APISuccessResponse(payload=payload.get("predictions"))


class PlaceDetailsView(APIView):
    """GET details for a place.

    Expects an `id` url parameter that contains the place id.

    Note the details are returned in Polish.

    Responses:
        - 200: Details for the place.
            - payload: Details for the place. See [here](https://developers.google.com/maps/documentation/places/web-service/details#PlacesDetailsResponse)
              for more information about the format of a place details response.
        - 404: Place not found.
        - 500: Internal server error.
    """

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
            return APIErrorResponse(status=404)

        if response.status_code != 200 or status != "OK":
            return APIErrorResponse(status=500)

        return APISuccessResponse(payload=payload.get("result"))
