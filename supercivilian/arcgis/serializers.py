from rest_framework import serializers


class ShelterSerializer(serializers.Serializer):
    """Serializer for `Shelter` objects."""

    id = serializers.IntegerField()
    longitude = serializers.FloatField()
    latitude = serializers.FloatField()
    distance = serializers.FloatField(required=False)
    inventory_type = serializers.CharField(required=False)
    access_type = serializers.CharField(required=False)
    area = serializers.IntegerField(required=False)
    capacity = serializers.IntegerField(required=False)
    quality = serializers.IntegerField(required=False)
    category = serializers.CharField(required=False)
    purpose = serializers.CharField(required=False)
    voivodeship = serializers.CharField(required=False)
    province = serializers.CharField(required=False)
    address = serializers.CharField(required=False)
