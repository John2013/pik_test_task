from django.contrib.gis.geos import Point
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.request import Request
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

    @action(detail=False)
    def in_point(self, request: Request):
        query_params = tuple(map(request.query_params.get, ("lat", "lon")))
        if None in query_params:
            return Response(
                {"message": "query params `lat` and `lon` must be set"},
                status=status.HTTP_400_BAD_REQUEST,
                exception=ValueError("query params `lat` and `lon` must be set"),
            )
        try:
            latitude, longitude = tuple(map(float, query_params))
        except ValueError as error:
            return Response(
                {"message": "query params `lat` and `lon` must be float"},
                status=status.HTTP_400_BAD_REQUEST,
                exception=error,
            )
        point = Point((latitude, longitude))
        suppliers = self.queryset.filter(servicearea__geometry__contains=point)
        page = self.paginate_queryset(suppliers)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(suppliers, many=True)
        return Response(serializer.data)


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
