from __future__ import annotations

import dataclasses
import typing
import urllib.parse

import requests
from django.core.cache import cache

from .constants import BASE_ARCGIS_SHELTER_API_URL


@dataclasses.dataclass
class Shelter:
    """
    See [here](https://services-eu1.arcgis.com/HE4WRthd9CIPj0R8/ArcGIS/rest/services/schrony_csv/FeatureServer/0).

    ObjectID (type: esriFieldTypeInteger, alias: ObjectID, SQL Type: sqlTypeInteger, nullable: true, editable: true)
    Rodzaj_inw (type: esriFieldTypeString, alias: Rodzaj inwentaryzacji, SQL Type: sqlTypeNVarchar, length: 4000, nullable: true, editable: true)
    Możliwoś (type: esriFieldTypeString, alias: Rodzaj dojazdu do obiektu, SQL Type: sqlTypeNVarchar, length: 4000, nullable: true, editable: true)
    Powierzchn (type: esriFieldTypeInteger, alias: Szacowana powierzchnia m kw., SQL Type: sqlTypeInteger, nullable: true, editable: true)
    Pojemnoś_ (type: esriFieldTypeInteger, alias: Szacowana pojemność w osobach, SQL Type: sqlTypeInteger, nullable: true, editable: true)
    Subiektywn (type: esriFieldTypeInteger, alias: Ocena jakościowa obiektu, SQL Type: sqlTypeInteger, nullable: true, editable: true)
    Rodzaj_obi (type: esriFieldTypeString, alias: Kategoria obiektu, SQL Type: sqlTypeNVarchar, length: 4000, nullable: true, editable: true)
    Przeznacze (type: esriFieldTypeString, alias: Przeznaczenie (MZ), SQL Type: sqlTypeNVarchar, length: 4000, nullable: true, editable: true)
    Województ (type: esriFieldTypeString, alias: Województwo, SQL Type: sqlTypeNVarchar, length: 4000, nullable: true, editable: true)
    Powiat (type: esriFieldTypeString, alias: Powiat, SQL Type: sqlTypeNVarchar, length: 4000, nullable: true, editable: true)
    Adres (type: esriFieldTypeString, alias: Adres, SQL Type: sqlTypeNVarchar, length: 4000, nullable: true, editable: true)
    x (type: esriFieldTypeDouble, alias: x, SQL Type: sqlTypeFloat, nullable: true, editable: true)
    y (type: esriFieldTypeDouble, alias: y, SQL Type: sqlTypeFloat, nullable: true, editable: true)
    ObjectId2 (type: esriFieldTypeOID, alias: ObjectId2, SQL Type: sqlTypeInteger, length: 0, nullable: false, editable: false)
    """

    id: str
    longitude: float
    latitude: float
    inventory_type: str | None = None
    access_type: str | None = None
    area: int | None = None
    capacity: int | None = None
    quality: int | None = None
    category: str | None = None
    purpose: str | None = None
    voivodeship: str | None = None
    province: str | None = None
    address: str | None = None

    @classmethod
    def from_api_attributes(cls, attributes: dict[str, typing.Any]) -> Shelter:
        """Create a `Shelter` object from the attributes of an API response.

        Args:
            attributes: The attributes of the shelter.

        Returns:
            A `Shelter` object.
        """
        return cls(
            id=attributes["ObjectID"],
            longitude=attributes["x"],
            latitude=attributes["y"],
            inventory_type=attributes["Rodzaj_inw"],
            access_type=attributes["Możliwoś"],
            area=attributes["Powierzchn"],
            capacity=attributes["Pojemnoś_"],
            quality=attributes["Subiektywn"],
            category=attributes["Rodzaj_obi"],
            purpose=attributes["Przeznacze"],
            voivodeship=attributes["Województ"],
            province=attributes["Powiat"],
            address=attributes["Adres"],
        )


def generate_arcgis_shelter_api_url(**params: dict[str, typing.Any]) -> str:
    """Generate a URL for the ArcGIS shelter API.

    Args:
        **params: The query parameters.

    Returns:
        The generated URL.
    """
    return f"{BASE_ARCGIS_SHELTER_API_URL}?{
        urllib.parse.urlencode(
            {
                **params,
            }
        )
    }"


def get_shelters_from_cache(longitude: float, latitude: float) -> list[Shelter] | None:
    """Get shelters for a point from the cache.

    Args:
        longitude: The longitude of the point.
        latitude: The latitude of the point.

    Returns:
        A list of shelters, if the shelters exist, else `None`.
    """
    if (shelters := cache.get(f"shelters:{longitude},{latitude}")) is not None:
        return [
            Shelter.from_api_attributes(shelter["attributes"]) for shelter in shelters
        ]

    return None


def set_shelters_in_cache(
    longitude: float,
    latitude: float,
    shelters: list[dict[str, typing.Any]],
    timeout: int = 60 * 60,
) -> None:
    """Set shelters in the cache.

    Args:
        longitude: The longitude of the point.
        latitude: The latitude of the point.
        shelters: The shelters to set in the cache.
        timeout: The timeout of the cache. Defaults to 1 hour.
    """
    cache.set(f"shelters:{longitude},{latitude}", shelters, timeout=timeout)


def get_shelters_for_point(
    longitude: float, latitude: float, range_: float, offset: int = 0, limit: int = 10
) -> list[Shelter]:
    """Get shelters within a given range of a point.

    Args:
        longitude: The longitude of the point.
        latitude: The latitude of the point.
        range_: The range in meters.
        offset: The offset of the first record to return. Defaults to 0.
        limit: The maximum number of records to return. Defaults to 10.

    Returns:
        A list of shelters.
    """
    if (shelters := get_shelters_from_cache(longitude, latitude)) is not None:
        return shelters[offset : offset + limit]

    url = generate_arcgis_shelter_api_url(
        where="1=1",
        geometryType="esriGeometryPoint",
        spatialRel="esriSpatialRelIntersects",
        geometry=f"{longitude},{latitude}",
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
        response = requests.get(url)
        payload = response.json()
    except requests.RequestException:
        return []

    if response.status_code != 200 or "features" not in payload:
        return []

    shelters = [
        Shelter.from_api_attributes(feature["attributes"])
        for feature in payload["features"]
    ]

    set_shelters_in_cache(longitude, latitude, shelters)

    return shelters[offset : offset + limit]


def get_details_for_shelter(id: int) -> Shelter | None:
    """Get details for a shelter.

    Args:
        The ID of the shelter.

    Returns:
        A `Shelter` object, if the shelter exists, else `None`.
    """
    if (shelter := cache.get(f"shelter:{id}")) is not None:
        return Shelter.from_api_attributes(shelter["attributes"])

    url = generate_arcgis_shelter_api_url(
        where=f"ObjectID = {id}",
        outFields="*",
        f="pjson",
    )

    try:
        response = requests.get(url)
        payload = response.json()
    except requests.RequestException:
        return None

    if response.status_code != 200 or "features" not in payload:
        return None

    shelter = Shelter.from_api_attributes(payload["features"][0]["attributes"])

    cache.set(f"shelter:{id}", payload["features"][0], timeout=60 * 60)

    return shelter
