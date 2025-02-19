from django.urls import path

from .views import PlaceDetailsView, PlacePhotoView, SearchAutoCompleteView

app_name = "google"

# fmt: off
urlpatterns = [
    path("search/autocomplete", SearchAutoCompleteView.as_view(), name="search-autocomplete"),
    path("places/<str:id>", PlaceDetailsView.as_view(), name="place-details"),
    path("photos/<str:reference>", PlacePhotoView.as_view(), name="place-photo"),
]
# fmt: on
