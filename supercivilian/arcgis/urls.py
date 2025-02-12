from django.urls import path

from .views import GetShelterDetailsView, GetSheltersForPointView

app_name = "arcgis"

# fmt: off
urlpatterns = [
    path("shelters", GetSheltersForPointView.as_view(), name="get-shelters-for-point"),
    path("shelters/<int:id>", GetShelterDetailsView.as_view(), name="get-shelter-details"),
]
# fmt: on
