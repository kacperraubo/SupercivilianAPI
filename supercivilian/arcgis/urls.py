from django.urls import path

from .views import GetSheltersForPointView

app_name = "arcgis"

# fmt: off
urlpatterns = [
    path("shelters", GetSheltersForPointView.as_view(), name="get-shelters-for-point"),
]
# fmt: on
