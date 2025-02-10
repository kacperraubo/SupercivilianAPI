from __future__ import annotations

import dataclasses

from geopy.distance import geodesic


@dataclasses.dataclass
class Point:
    """A point on the Earth.

    Attributes:
        longitude: The longitude of the point.
        latitude: The latitude of the point.
    """

    longitude: float
    latitude: float

    def __str__(self) -> str:
        """The string representation of the point.

        Returns:
            A string representation of the point.
        """
        return f"{self.longitude},{self.latitude}"

    def distance(self, point: Point) -> float:
        """Get the distance between this point and another point.

        Args:
            point: The point to get the distance to.

        Returns:
            The distance between the two points in meters.
        """
        return geodesic(
            (self.latitude, self.longitude),
            (point.latitude, point.longitude),
        ).meters
