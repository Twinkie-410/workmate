from django.contrib.auth import get_user_model
from django.db import models


class CatBreed(models.Model):
    name = models.CharField(max_length=255, blank=True, verbose_name="название")

    class Meta:
        verbose_name = "порода"
        verbose_name_plural = "породы"

    def __str__(self):
        return self.name


class Cat(models.Model):
    breed = models.ForeignKey(CatBreed, on_delete=models.SET_NULL, null=True, blank=False, verbose_name="порода")
    owner = models.ForeignKey(
        get_user_model(), on_delete=models.SET_NULL, null=True, blank=False, verbose_name="владелец"
    )

    name = models.CharField(max_length=255, blank=True, verbose_name="имя")
    colour = models.CharField(max_length=255, blank=False, verbose_name="окрас")
    age_month = models.PositiveIntegerField(verbose_name="возраст - полных месяцев")
    description = models.TextField(blank=True, verbose_name="описание")

    class Meta:
        verbose_name = "котёнок"
        verbose_name_plural = "котята"

    def __str__(self):
        return self.name
