from rest_framework import serializers


class AutocompletePredictionSerializer(serializers.Serializer):
    """Serializer for `AutocompletePrediction` objects."""

    description = serializers.CharField()
    place_id = serializers.CharField()
    types = serializers.ListField(child=serializers.CharField(), required=False)


class PlacePhotoSerializer(serializers.Serializer):
    """Serialize for `PlacePhoto` objects."""

    reference = serializers.CharField()
    height = serializers.IntegerField()
    width = serializers.IntegerField()


class PlaceDetailsSerializer(serializers.Serializer):
    """Serializer for `PlaceDetails` objects."""

    id = serializers.CharField()
    name = serializers.CharField()
    url = serializers.CharField()
    formatted_address = serializers.CharField()
    website = serializers.CharField(required=False)
    latitude = serializers.FloatField()
    longitude = serializers.FloatField()
    photos = PlacePhotoSerializer(many=True, required=False)


class GeocodePlaceSerializer(serializers.Serializer):
    """Serializer for `GeocodePlace` objects."""

    id = serializers.CharField()
    latitude = serializers.FloatField()
    longitude = serializers.FloatField()
    address = serializers.CharField()
