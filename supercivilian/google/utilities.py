import typing
import urllib.parse

from django.conf import settings

from .constants import BASE_PLACES_API_URL


def generate_places_api_url(url: str, **params: dict[str, typing.Any]) -> str:
    """Generate a URL for the Google Places API.

    This function automatically appends the API key to the query parameters.

    Args:
        url: The endpoint URL.
        params: The query parameters.

    Returns:
        The generated URL.
    """
    return f"{BASE_PLACES_API_URL}{url}?{
        urllib.parse.urlencode(
            {
                **params,
                'key': settings.MAPS_PLATFORM_API_KEY,
            }
        )
    }"
