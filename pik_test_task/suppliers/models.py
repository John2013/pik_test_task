from django.contrib.gis.db.models import PolygonField
from django.db import models


class Supplier(models.Model):
    class Meta:
        verbose_name = "Поставщик"
        verbose_name_plural = "Поставщики"

    name = models.CharField("Название организации", max_length=255, unique=True)
    email = models.CharField(max_length=255)
    phone = models.CharField("Номер телефона", max_length=20)
    address = models.TextField("Адрес центрального офиса")

    def __str__(self):
        return str(self.name)


class ServiceType(models.Model):
    class Meta:
        verbose_name = "Тип услуг"
        verbose_name_plural = "Типы услуг"

    name = models.CharField("Название", max_length=255, unique=True)

    def __str__(self):
        return str(self.name)


class ServiceArea(models.Model):
    class Meta:
        verbose_name = "Область обслуживания"
        verbose_name_plural = "Области обслуживания"

    supplier = models.ForeignKey("Supplier", on_delete=models.CASCADE)
    name = models.CharField("Название", max_length=255)
    types = models.ManyToManyField(
        ServiceType, through="TypeInArea", verbose_name="Типы обслуживания"
    )
    geometry = PolygonField("Область")

    def __str__(self):
        return str(self.name)


class TypeInArea(models.Model):
    area = models.ForeignKey(ServiceArea, on_delete=models.CASCADE)
    service_type = models.ForeignKey(ServiceType, on_delete=models.CASCADE)
    price = models.IntegerField("цена обслуживания за единицу оказываемой услуги")

    def __str__(self):
        return f"<Type {self.service_type} in area {self.area} (f{self.price})>"
