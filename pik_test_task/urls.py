from django.urls import path, include
from rest_framework import routers

from .suppliers import views

router = routers.DefaultRouter()
router.register(r"suppliers", views.SupplierViewSet)
router.register(r"areas", views.ServiceAreaViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path("api-auth/", include("rest_framework.urls", namespace="rest_framework")),
]
