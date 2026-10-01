from rest_framework import serializers
from rest_framework import fields

from .models import Room, Building, Tenant, Tariff, UtilityReading, Lease


class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ['id', 'building', 'number']


class BuildingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Building
        fields = ['id', 'street']


class TenantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tenant
        fields = ['id', 'user', 'first_name', 'last_name']


class TariffSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tariff
        fields = '__all__'


class UtilityReadingSerializer(serializers.ModelSerializer):
    class Meta:
        model = UtilityReading
        fields = '__all__'


class LeaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lease
        fields = '__all__'