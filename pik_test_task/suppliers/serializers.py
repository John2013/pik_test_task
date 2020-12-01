from rest_framework import serializers

from .models import Supplier, ServiceArea, ServiceType


class SupplierSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Supplier
        fields = ["name", "email", "phone", "address", "servicearea"]


class ServiceTypeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ServiceType
        fields = ["name"]


class ServiceAreaSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ServiceArea
        fields = ["supplier", "name", "price", "servicetypes", "geometry"]