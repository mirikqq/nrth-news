from django.db import models
from django.utils import timezone


class News(models.Model):
    """Модель новости"""
    photo = models.ImageField(upload_to='news_photos/', blank=True, null=True, verbose_name='Фотография')
    title = models.CharField(max_length=250, verbose_name='Название новости')
    short_description = models.TextField(verbose_name='Краткое описание')
    full_description = models.TextField(verbose_name='Полное описание')
    pub_date = models.DateTimeField(default=timezone.now, verbose_name='Дата публикации')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-pub_date']
        verbose_name = 'Новость'
        verbose_name_plural = 'Новости'

    def __str__(self):
        return self.title


class Visitor(models.Model):
    """Модель посетителя с геолокацией"""
    ip_address = models.GenericIPAddressField(verbose_name='IP адрес')
    city = models.CharField(max_length=100, blank=True, default='', verbose_name='Город')
    region = models.CharField(max_length=100, blank=True, default='', verbose_name='Регион')
    country = models.CharField(max_length=100, blank=True, default='', verbose_name='Страна')
    country_code = models.CharField(max_length=10, blank=True, default='', verbose_name='Код страны')
    latitude = models.FloatField(null=True, blank=True, verbose_name='Широта')
    longitude = models.FloatField(null=True, blank=True, verbose_name='Долгота')
    visited_at = models.DateTimeField(auto_now_add=True, verbose_name='Время визита')
    user_agent = models.TextField(blank=True, default='', verbose_name='User Agent')

    class Meta:
        ordering = ['-visited_at']
        verbose_name = 'Посетитель'
        verbose_name_plural = 'Посетители'

    def __str__(self):
        location = self.city or self.country or 'Unknown'
        return f'{self.ip_address} — {location} ({self.visited_at.strftime("%d.%m.%Y %H:%M")})'
