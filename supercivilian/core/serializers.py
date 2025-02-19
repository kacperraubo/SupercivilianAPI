from rest_framework import serializers

from .utilities import error_response_serializer


ErrorWithMessageSerializer = error_response_serializer(
    name="ErrorWithMessage",
    error={
        "message": serializers.CharField(required=True),
    },
)
