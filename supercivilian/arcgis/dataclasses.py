from __future__ import annotations

import dataclasses
import typing

from supercivilian.core.dataclasses import Point

from .typing import ArcGISShelter


@dataclasses.dataclass(frozen=True)
class Shelter:
    """Our wrapper around the shelter data returned by the ArcGIS API.

    See `supercivilian.arcgis.typing.ArcGISShelter` for the raw API return data.
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

    @property
    def point(self) -> Point:
        """The point of the shelter.

        Returns:
            A `Point` object.
        """
        return Point(longitude=self.longitude, latitude=self.latitude)

    @classmethod
    def from_api_data(cls, shelter: ArcGISShelter) -> Shelter:
        """Create a `Shelter` object from an ArcGIS shelter.

        Args:
            attributes: The attributes of the shelter.

        Returns:
            A `Shelter` object.
        """
        attributes = shelter["attributes"]

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

    def dict(self, point: Point | None = None) -> dict[str, typing.Any]:
        """Convert the `Shelter` object to a dictionary.

        Args:
            point: If provided, the distance to the point will be added to the
                dictionary under the key `distance`.

        Returns:
            A dictionary representation of the `Shelter` object.
        """
        _dict = dataclasses.asdict(self)

        if point is not None:
            _dict["distance"] = point.distance(self.point)

        return _dict
