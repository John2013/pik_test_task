from rest_framework import viewsets, permissions

from .models import Supplier, ServiceArea, ServiceType, TypeInArea
from .serializers import (
    SupplierSerializer,
    ServiceAreaSerializer,
    ServiceTypeSerializer, TypeInAreaSerializer,
)


class SupplierViewSet(viewsets.ModelViewSet):
    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializer
    permission_classes = [permissions.IsAuthenticated]


class ServiceAreaViewSet(viewsets.ModelViewSet):
    queryset = ServiceArea.objects.all()
    serializer_class = ServiceAreaSerializer
    permission_classes = [permissions.IsAuthenticated]


class ServiceTypeViewSet(viewsets.ModelViewSet):
    queryset = ServiceType.objects.all()
    serializer_class = ServiceTypeSerializer
    permission_classes = [permissions.IsAuthenticated]


class TypeInAreaViewSet(viewsets.ModelViewSet):
    queryset = TypeInArea.objects.all()
    serializer_class = TypeInAreaSerializer
    permission_classes = [permissions.IsAuthenticated]
