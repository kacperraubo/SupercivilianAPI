from django.contrib import admin
from django.urls import include, path

# fmt: off
urlpatterns = [
    path("admin/", admin.site.urls),
    path("google/", include("supercivilian.google.urls")),
    path("arcgis/", include("supercivilian.arcgis.urls")),
    path("shelters/", include("supercivilian.shelters.urls")),
]
# fmt: on
