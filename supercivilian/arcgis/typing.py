import typing


class ArcGISShelterAttributes(typing.TypedDict):
    """The attributes of a shelter returned by the ArcGIS API.

    See [here](https://services-eu1.arcgis.com/HE4WRthd9CIPj0R8/ArcGIS/rest/services/schrony_csv/FeatureServer/0)
    for more information about the attributes.
    """

    ObjectID: int
    Rodzaj_inw: str | None
    Możliwoś: str | None
    Powierzchn: int | None
    Pojemnoś_: int | None
    Subiektywn: int | None
    Rodzaj_obi: str | None
    Przeznacze: str | None
    Województ: str | None
    Powiat: str | None
    Adres: str | None
    x: float
    y: float


class ArcGISShelterGeometry(typing.TypedDict):
    """The geometry of a shelter returned by the ArcGIS API."""

    x: float
    y: float


class ArcGISShelter(typing.TypedDict):
    """A shelter returned by the ArcGIS API."""

    attributes: ArcGISShelterAttributes
    geometry: ArcGISShelterGeometry
