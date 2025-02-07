import typing
from django.core.cache import cache
from django.forms import model_to_dict
from django.http import Http404, HttpRequest, HttpResponse
from django.shortcuts import render
from django.views.generic import View, TemplateView

from supercivilian.arcgis.utilities import (
    get_details_for_shelter,
    get_shelters_from_cache,
)
from supercivilian.core.responses import (
    APIErrorResponse,
    APIResponse,
    APISuccessResponse,
)

from .models import Shelter
from .constants import WARSAW_COORDINATES


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


class ShelterListView(TemplateView):
    template_name = "shelters/list.html"

    def get_context_data(self, **kwargs: typing.Any) -> dict[str, typing.Any]:
        context = super().get_context_data(**kwargs)

        if (
            shelters := get_shelters_from_cache(
                WARSAW_COORDINATES.longitude, WARSAW_COORDINATES.latitude
            )
        ) is not None:
            context["shelters"] = shelters

        return context
