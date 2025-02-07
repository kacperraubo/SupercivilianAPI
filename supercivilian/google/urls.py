from django.urls import path

from .views import PlaceDetailsView, SearchAutoCompleteView

app_name = "google"

# fmt: off
urlpatterns = [
    path("search/autocomplete", SearchAutoCompleteView.as_view(), name="search-autocomplete"),
    path("places/<str:id>", PlaceDetailsView.as_view(), name="place-details"),
]
# fmt: on
