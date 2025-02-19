import dataclasses


@dataclasses.dataclass
class AutocompletePrediction:
    """Our wrapper around the data returned from the Google Places Search
    Autocomplete endpoint.
    """

    place_id: str
    description: str
    types: list[str] | None = None


@dataclasses.dataclass
class PlacePhoto:
    """Our wrapper around Google's `PlacePhoto` object."""

    reference: str
    height: int
    width: int


@dataclasses.dataclass
class PlaceDetails:
    """Our wrapper around the data returned from the Google Places Details
    endpoint.
    """

    id: str
    latitude: float
    longitude: float
    name: str
    url: str
    formatted_address: str
    website: str | None = None
    photos: list[PlacePhoto] | None = None
