from django.db import models


class Supplier(models.Model):
    class Meta:
        verbose_name = "Поставщик"
        verbose_name_plural = "Поставщики"

    name = models.CharField("Название организации", max_length=255, unique=True)
    email = models.CharField(max_length=255)
    phone = models.CharField("Номер телефона", max_length=20)
    address = models.TextField("Адрес центрального офиса")


class ServiceType(models.Model):
    class Meta:
        verbose_name = "Тип услуг"
        verbose_name_plural = "Типы услуг"

    name = models.CharField("Название", max_length=255, unique=True)


class ServiceArea(models.Model):
    class Meta:
        verbose_name = "Область обслуживания"
        verbose_name_plural = "Области обслуживания"

    supplier = models.ForeignKey("Supplier", on_delete=models.CASCADE)
    name = models.CharField("Название", max_length=255)
    services = models.ManyToManyField(
        ServiceType, through="AreaService", verbose_name="Типы обслуживания"
    )
    geometry = models.JSONField("Область")


class AreaService(models.Model):
    area = models.ForeignKey(
        ServiceArea, on_delete=models.CASCADE, related_name="areaservice"
    )
    service_type = models.ForeignKey(
        ServiceType, on_delete=models.CASCADE, related_name="areaservice"
    )
    price = models.IntegerField("цена обслуживания за единицу оказываемой услуги")
