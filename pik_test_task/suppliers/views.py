from typing import Optional

from django.contrib.gis.geos import Point
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response

from .models import Supplier, ServiceArea, ServiceType, TypeInArea
from .serializers import (
    SupplierSerializer,
    ServiceAreaSerializer,
    ServiceTypeSerializer,
    TypeInAreaSerializer,
)


class SupplierViewSet(viewsets.ModelViewSet):
    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = Supplier.objects.all()
        # noinspection PyTypeChecker
        point_query_params: tuple[Optional[str]] = tuple(
            map(self.request.query_params.get, ("lat", "lon"))
        )
        if None not in point_query_params:
            try:
                latitude, longitude = tuple(map(float, point_query_params))
            except ValueError as error:
                return Response(
                    {"message": "query params `lat` and `lon` must be float"},
                    status=status.HTTP_400_BAD_REQUEST,
                    exception=error,
                )
            point = Point((latitude, longitude))
            queryset = queryset.filter(servicearea__geometry__contains=point)

        return queryset


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
