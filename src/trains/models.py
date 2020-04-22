from django.db import models
from django.core.exceptions import ValidationError
from cities.models import City


class Train(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name='Номер потягу')
    from_city = models.ForeignKey(City, on_delete=models.CASCADE,
                                    verbose_name='Звідки', related_name='from_city')
    to_city = models.ForeignKey(City, on_delete=models.CASCADE,
                                    verbose_name='Куди', related_name='to_city')
    travel_time = models.IntegerField(verbose_name='Час в дорозі')

    class Meta:
        verbose_name = 'Потяг'
        verbose_name_plural = 'Потяги'
        ordering = ['name']

    def __str__(self):
        return f'Потяг №{self.name} із {self.from_city} в {self.to_city}'

    def clean(self, *args, **kwargs):
        if self.from_city == self.to_city:
            raise ValidationError('Змініть місто прибуття')
        qs = Train.objects.filter(from_city=self.from_city,
                                    to_city=self.to_city,
                                    travel_time=self.travel_time).exclude(pk=self.pk)
        if qs.exists():
            raise ValidationError('Змініть час в дорозі')

        def save(self, *args, **kwargs):
            self.clean()
            super().save(*args, **kwargs)
