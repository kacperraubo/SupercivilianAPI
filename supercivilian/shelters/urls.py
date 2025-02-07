from django.urls import path

from .views import ShelterAPIDetailView, ShelterDetailView, ShelterListView

app_name = "shelters"

# fmt: off
urlpatterns = [
    path("", ShelterListView.as_view(), name="list"),
    path("<int:id>", ShelterDetailView.as_view(), name="detail"),
    path("api/<int:id>", ShelterAPIDetailView.as_view(), name="api-detail"),
]
# fmt: on
