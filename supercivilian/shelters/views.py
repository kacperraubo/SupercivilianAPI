from django.forms import model_to_dict
from django.http import Http404, HttpRequest, HttpResponse
from django.shortcuts import render
from django.views.generic import View

from supercivilian.arcgis.utilities import get_details_for_shelter
from supercivilian.core.responses import (
    APIErrorResponse,
    APIResponse,
    APISuccessResponse,
)

from .models import Shelter


class ShelterDetailView(View):
    """Get details for a shelter."""

    def get(self, request: HttpRequest, id: int) -> HttpResponse:
        shelter = get_details_for_shelter(id)

        if shelter is None:
            raise Http404("Shelter not found")

        model = Shelter.objects.filter(id=id).first()

        return render(
            request, "shelters/detail.html", {"shelter": shelter, "model": model}
        )


class ShelterAPIDetailView(View):
    """Get details stored in our database for a shelter."""

    def get(self, request: HttpRequest, id: int) -> APIResponse:
        try:
            shelter = Shelter.objects.get(id=id)
        except Shelter.DoesNotExist:
            return APIErrorResponse(status=404)

        return APISuccessResponse(payload=model_to_dict(shelter))
