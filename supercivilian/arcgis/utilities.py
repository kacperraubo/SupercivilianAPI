from __future__ import annotations

import typing
import logging
import urllib.parse

import requests
from django.core.cache import cache

from supercivilian.core.dataclasses import Point

from .constants import BASE_ARCGIS_SHELTER_API_URL
from .dataclasses import Shelter
from .typing import ArcGISShelter

logger = logging.getLogger(__name__)


def _shelters_cache_key_for_point(point: Point) -> str:
    """Generate a cache key for shelters for a point.

    Args:
        point: The point.
    """
    return f"shelters:{point.longitude},{point.latitude}"


def _geodesic_sort(point: Point) -> float:
    """Closure for sorting shelters by distance from a point.

    Args:
        point: The point to sort shelters by distance from.

    Returns:
        A function that can be used as a `key` argument to `sorted` for a list
        of `Shelter` objects.
    """

    def closure(shelter: Shelter) -> float:
        return point.distance(shelter.point)

    return closure


def generate_arcgis_shelter_api_url(**params: typing.Any) -> str:
    """Generate a URL for the ArcGIS shelter API.

    Args:
        **params: The query parameters to append to the URL.

    Returns:
        The generated URL with encoded parameters.
    """
    return f"{BASE_ARCGIS_SHELTER_API_URL}?{urllib.parse.urlencode(params)}"


def get_shelters_from_cache(point: Point) -> list[Shelter] | None:
    """Get shelters for a point from the cache.

    Args:
        point: The point.

    Returns:
        A list of `Shelter` objects if the shelters exist, else `None`.
    """
    if (shelters := cache.get(_shelters_cache_key_for_point(point))) is not None:
        return [Shelter(**shelter) for shelter in shelters]

    return None


def set_shelters_in_cache(
    point: Point,
    shelters: list[Shelter],
    timeout: int = 60 * 60,
    sort: bool = True,
) -> None:
    """Set shelters for a point in the cache.

    Args:
        point: The point.
        shelters: The shelters to set in the cache.
        timeout: The timeout of the cache. Defaults to 1 hour.
        sort: Whether to sort the shelters by distance from the point before
            setting them in the cache. Defaults to `True`.
    """
    if sort:
        shelters.sort(key=_geodesic_sort(point))

    cache.set(
        _shelters_cache_key_for_point(point),
        [shelter.dict() for shelter in shelters],
        timeout=timeout,
    )


def get_shelters_for_point(
    point: Point, range_: float, offset: int = 0, limit: int = 10
) -> list[Shelter]:
    """Get shelters within a given range of a point from the cache or the
    ArcGIS API.

    Args:
        point: The point to search around.
        range_: The range in meters.
        offset: The offset of the first record to return. Defaults to 0.
        limit: The maximum number of records to return. Defaults to 10.

    Returns:
        A list of shelters sorted by distance from the point.
    """
    if (shelters := get_shelters_from_cache(point)) is not None:
        return shelters[offset : offset + limit]

    url = generate_arcgis_shelter_api_url(
        where="1=1",
        geometryType="esriGeometryPoint",
        spatialRel="esriSpatialRelIntersects",
        geometry=f"{point.longitude},{point.latitude}",
        inSR=4326,
        distance=range_,
        units="esriSRUnit_Meter",
        outFields="*",
        returnGeometry="true",
        orderByFields="ObjectID ASC",
        resultRecordCount="",
        resultType="standard",
        multipatchOption="xyFootprint",
        f="pjson",
    )

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()

        payload = response.json()

        if "features" not in payload:
            return []

        features: list[ArcGISShelter] = payload["features"]
    except (requests.RequestException, ValueError):
        return []

    shelters = [Shelter.from_api_data(feature) for feature in features]
    sorted_shelters = sorted(shelters, key=_geodesic_sort(point))

    set_shelters_in_cache(point, sorted_shelters, sort=False)

    return sorted_shelters[offset : offset + limit]


def get_details_for_shelter(id: int) -> Shelter | None:
    """Get details for a shelter.

    Args:
        id: The ID of the shelter.

    Returns:
        A `Shelter` object if the shelter exists, else `None`.
    """
    cache_key = f"shelter:{id}"

    if (shelter := cache.get(cache_key)) is not None:
        return Shelter(**shelter)

    url = generate_arcgis_shelter_api_url(
        where=f"ObjectID = {id}",
        outFields="*",
        f="pjson",
    )

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()

        payload = response.json()

        if "features" not in payload:
            return None

        features: list[ArcGISShelter] = payload["features"]
    except (requests.RequestException, ValueError):
        return None

    if len(features) == 0:
        return None

    shelter = Shelter.from_api_data(features[0])
    cache.set(cache_key, shelter.dict(), timeout=60 * 60)

    return shelter
