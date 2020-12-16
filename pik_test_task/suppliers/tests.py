from typing import Iterable
import http

from django.contrib.auth.models import User
from django.contrib.gis.geos import Polygon, Point
from django.test import TestCase
from faker import Faker
from rest_framework.test import APIClient
from rest_framework.reverse import reverse

from pik_test_task.suppliers.models import Supplier, ServiceType, ServiceArea

POLYGON_TEMPLATE = """
{
  "type": "Polygon",
  "coordinates": [
    [
      [
        {lat1},
        {lon1}
      ],
      [
        {lat2},
        {lon2}
      ],
      [
        {lat3},
        {lon3}
      ],
      [
        {lat4},
        {lon4}
      ],
      [
        {lat1},
        {lon1}
      ]
    ]
  ]
}  
"""


def create_test_suppliers(service_types: Iterable[ServiceType]):
    fake = Faker()
    Faker.seed(0)

    types = []
    for _ in range(5):
        types.append(ServiceType.objects.create(name=fake.unique.word()))

    suppliers = []
    for number in range(10):
        supplier = Supplier.objects.create(
            name=fake.unique.company(),
            email=fake.unique.email(),
            phone=fake.unique.phone_number()[:20],
            address=fake.unique.address(),
        )
        start_lat = number
        start_lon = number
        polygon = Polygon(
            (
                (start_lat, start_lon),
                (start_lat + 1, start_lon),
                (start_lat + 1, start_lon + 1),
                (start_lat, start_lon + 1),
                (start_lat, start_lon),
            )
        )

        supplier.servicearea_set.create(name=fake.unique.company(), geometry=polygon)
        suppliers.append(supplier)
    return suppliers


class SuppliersTest(TestCase):
    def setUp(self) -> None:
        self.user = User.objects.create_user(username="test_user")
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_creating_supplier(self):
        response = self.client.post(
            "/suppliers/",
            {
                "name": "test",
                "email": "test@test.ru",
                "phone": "+79910555500",
                "address": "address",
                "servicearea_set": [],
            },
        )
        self.assertEqual(response.status_code, http.HTTPStatus.CREATED)
        supplier = Supplier.objects.last()
        self.assertEqual(supplier.name, "test")

    def test_creating_type(self):
        response = self.client.post("/types/", {"name": "type1"})
        self.assertEqual(response.status_code, http.HTTPStatus.CREATED)
        type = ServiceType.objects.last()
        self.assertEqual(type.name, "type1")

    def test_creating_area(self):
        fake = Faker()
        Faker.seed(0)

        supplier = Supplier.objects.create(
            name=fake.unique.company(),
            email=fake.unique.email(),
            phone=fake.unique.phone_number(),
            address=fake.unique.address(),
        )
        response = self.client.post(
            "/areas/",
            {
                "supplier": reverse("supplier-detail", [supplier.pk]),
                "name": "test",
                "types": [],
                "geometry": (
                    "{\n"
                    '  "type": "Polygon",\n'
                    '  "coordinates": [\n'
                    "    [\n"
                    "      [\n"
                    "        37.901201248168945,\n"
                    "        59.088825146044556\n"
                    "      ],\n"
                    "      [\n"
                    "        37.918453216552734,\n"
                    "        59.088825146044556\n"
                    "      ],\n"
                    "      [\n"
                    "        37.918453216552734,\n"
                    "        59.09596730040326\n"
                    "      ],\n"
                    "      [\n"
                    "        37.901201248168945,\n"
                    "        59.09596730040326\n"
                    "      ],\n"
                    "      [\n"
                    "        37.901201248168945,\n"
                    "        59.088825146044556\n"
                    "      ]\n"
                    "    ]\n"
                    "  ]\n"
                    "}"
                ),
            },
        )
        self.assertEqual(response.status_code, http.HTTPStatus.CREATED, response.json())
        area = ServiceArea.objects.last()
        self.assertEqual(area.name, "test")

    def test_returning_suppliers_with_area_in_point(self):
        types = []
        for type_number in range(5):
            types.append(ServiceType.objects.create(name=f"type_{type_number}"))

        create_test_suppliers(types)

        point = Point((3.5, 3.5))

        response = self.client.get(
            f"/suppliers/in_point/?lat={point[0]}&lon={point[1]}"
        )
        self.assertEqual(response.status_code, http.HTTPStatus.OK)
        self.assertEqual(response.json()["count"], 1, "неверное количество поставщиков")
