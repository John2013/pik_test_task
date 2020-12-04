from rest_framework import serializers

from .models import Supplier, ServiceArea, ServiceType, TypeInArea


class SupplierSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Supplier
        fields = ["id", "name", "email", "phone", "address", "servicearea_set"]


class ServiceTypeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ServiceType
        fields = ["id", "name"]


class TypeInAreaSerializer(serializers.HyperlinkedModelSerializer):
    area_name = serializers.StringRelatedField(source="area")
    type_name = serializers.StringRelatedField(source="service_type")

    class Meta:
        model = TypeInArea
        fields = ["area", "area_name", "service_type", "type_name", "price"]


class ServiceAreaSerializer(serializers.HyperlinkedModelSerializer):
    types = serializers.StringRelatedField(many=True)
    typeinarea_set = TypeInAreaSerializer(many=True, read_only=True)

    class Meta:
        model = ServiceArea
        fields = ["id", "supplier", "name", "types", "typeinarea_set", "geometry"]
