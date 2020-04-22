from django.db import models


class City(models.Model):
    """Місто"""
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Місто'
        verbose_name_plural = 'Міста'
        ordering = ['name']
