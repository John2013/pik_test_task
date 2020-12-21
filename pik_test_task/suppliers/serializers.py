from rest_framework import serializers

from .models import Supplier, ServiceArea, ServiceType, TypeInArea


class ServiceTypeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ServiceType
        fields = ["id", "name"]


class TypeInAreaSlimSerializer(serializers.HyperlinkedModelSerializer):
    type_name = serializers.StringRelatedField(source="service_type")

    class Meta:
        model = TypeInArea
        fields = ["service_type", "type_name", "price"]


class TypeInAreaSerializer(TypeInAreaSlimSerializer):
    area_name = serializers.StringRelatedField(source="area")

    class Meta:
        model = TypeInArea
        fields = ["area", "area_name", "service_type", "type_name", "price"]


class ServiceAreaSerializer(serializers.HyperlinkedModelSerializer):
    types = serializers.StringRelatedField(many=True)
    typeinarea_set = TypeInAreaSlimSerializer(many=True, read_only=True)

    class Meta:
        model = ServiceArea
        fields = ["id", "supplier", "name", "types", "typeinarea_set", "geometry"]


class SupplierSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Supplier
        fields = ["id", "name", "email", "phone", "address", "servicearea_set"]
        extra_kwargs = {"lat": {"write_only": True}, "lon": {"write_only": True}}
