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
    if (shelters := cache.get(f"shelters:{longitude},{latitude}")) is not None:
        return [Shelter(**shelter) for shelter in shelters[offset : offset + limit]]

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
        Shelter(
            id=feature["attributes"]["ObjectID"],
            inventory_type=feature["attributes"]["Rodzaj_inw"],
            access_type=feature["attributes"]["Możliwoś"],
            area=feature["attributes"]["Powierzchn"],
            capacity=feature["attributes"]["Pojemnoś_"],
            quality=feature["attributes"]["Subiektywn"],
            category=feature["attributes"]["Rodzaj_obi"],
            purpose=feature["attributes"]["Przeznacze"],
            voivodeship=feature["attributes"]["Województ"],
            province=feature["attributes"]["Powiat"],
            address=feature["attributes"]["Adres"],
            longitude=feature["geometry"]["x"],
            latitude=feature["geometry"]["y"],
        )
        for feature in payload["features"]
    ]

    cache.set(
        f"shelters:{longitude},{latitude}",
        [dataclasses.asdict(shelter) for shelter in shelters],
        timeout=60 * 60,
    )

    return shelters[offset : offset + limit]
