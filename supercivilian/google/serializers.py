from rest_framework import serializers


class AutocompletePredictionSerializer(serializers.Serializer):
    """Serializer for `AutocompletePrediction` objects."""

    description = serializers.CharField()
    place_id = serializers.CharField()
    types = serializers.ListField(child=serializers.CharField(), required=False)


class PlaceDetailsSerializer(serializers.Serializer):
    """Serializer for `PlaceDetails` objects."""

    id = serializers.CharField()
    name = serializers.CharField()
    url = serializers.CharField()
    formatted_address = serializers.CharField()
    website = serializers.CharField(required=False)
