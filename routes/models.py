from django.db import models
from trains.models import Train


class Route(models.Model):
    """Маршрут"""
    name = models.CharField(max_length=100,
                            verbose_name='Назва маршруту', unique=True)
    from_city = models.CharField(max_length=100,
                                 verbose_name='Звідки')
    to_city = models.CharField(max_length=100,
                               verbose_name='Куди')
    trains = models.ManyToManyField(Train, blank=True,
                                    verbose_name='Список потягів')
    travel_times = models.IntegerField(verbose_name='Час в дорозі')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Маршрут'
        verbose_name_plural = 'Маршрути'
        ordering = ['name']
