from django.contrib.auth.models import User
from django.test import TestCase
from faker import Faker
from rest_framework.test import APIClient

from pik_test_task.suppliers.models import Supplier, ServiceType


POLYGON_TEMPLATE = """
{
  "type": "FeatureCollection",
  "features": [
    {
      "type": "Feature",
      "properties": {},
      "geometry": {
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
    }
  ]
}
"""


def create_test_suppliers():
    fake = Faker()
    Faker.seed(0)

    types = []
    for _ in range(5):
        types.append(ServiceType.objects.create(name=fake.unique.word()))

    suppliers = []
    for _ in range(10):
        supplier = Supplier.objects.create(
            name=fake.unique.company(),
            email=fake.unique.email(),
            phone=fake.unique.phone(),
            address=fake.unique.address()
        )
        areas = []
        for _ in range(20):
            supplier.servicearea_set.create(
                name=fake.unique.company(),
                geometry="[]"
            )





class SuppliersTest(TestCase):
    def setUp(self) -> None:
        self.user = User.objects.create_user(username="test_user")
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_creating_suppliers(self):
        response = self.client.post(
            "/suppliers/",
            {
                "name": "test",
                "email": "test@test.ru",
                "phone": "+79910555500",
                "address": "address",
                "servicearea_set": "[]",
            },
        )

    def test_returning_suppliers_with_area_in_point(self):
        user = User.objects.create_user(username="test_user")
        client = APIClient()
        client.force_authenticate(user=user)
