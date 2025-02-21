from drf_spectacular.utils import inline_serializer
from rest_framework import serializers
from rest_framework.fields import Field


def success_response_serializer(
    name: str,
    payload: dict[str, serializers.Field] | None = None,
    many: bool = False,
    serializer: serializers.Serializer | None = None,
) -> serializers.Serializer:
    """Function for creating inline serializers for success responses.

    Args:
        name: The name of the serializer.
        payload: The payload to include in the serializer.
            Defaults to `None`.
        many: Whether the payload is a list of items.
            Defaults to `False`.
        serializer: The serializer to use for the payload.
            If provided, the `payload` argument will be ignored.
            Defaults to `None`.

    Returns:
        A `Serializer` instance.
    """
    if serializer is None:
        payload_serializer = inline_serializer(name=f"{name}Payload", fields=payload)
    else:
        payload_serializer = serializer()

    return inline_serializer(
        name=name,
        fields={
            "success": serializers.BooleanField(default=True),
            "payload": (
                serializers.ListField(
                    child=payload_serializer,
                )
                if many
                else payload_serializer
            ),
        },
    )


def error_response_serializer(
    name: str,
    error: dict[str, Field] | None = None,
    serializer: serializers.Serializer | None = None,
) -> serializers.Serializer:
    """Function for creating inline serializers for error responses.

    Args:
        name: The name of the serializer.
        error: The error to include in the serializer.
            Defaults to `None`.
        serializer: The serializer to use for the error.
            If provided, the `error` argument will be ignored.
            Defaults to `None`.

    Returns:
        A `Serializer` instance.
    """
    if serializer is None:
        error_serializer = inline_serializer(name=f"{name}Error", fields=error)
    else:
        error_serializer = serializer()

    return inline_serializer(
        name=name,
        fields={
            "success": serializers.BooleanField(default=False),
            "error": error_serializer,
        },
    )
