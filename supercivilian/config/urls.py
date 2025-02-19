from django.urls import include, path
from drf_spectacular.views import SpectacularRedocView, SpectacularAPIView

# fmt: off
urlpatterns = [
    path("google/", include("supercivilian.google.urls")),
    path("arcgis/", include("supercivilian.arcgis.urls")),
    path("schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "",
        SpectacularRedocView.as_view(),
        name="openapi-schema",
    ),
]
# fmt: on
