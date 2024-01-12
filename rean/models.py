from django.conf import settings
from django.db import models
from django.utils import timezone

class Rean(models.Model):
    author      = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title_file    = models.CharField(max_length=200)
    title_dif     = models.CharField(max_length=4)
    title_th     = models.CharField(max_length=200)
    title_ru     = models.CharField(max_length=200)
    title_is     = models.CharField(max_length=200)
    text_note = models.TextField()
    text_ph   = models.TextField()
    text_ex   = models.TextField()
    created_date    = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()
        
    #после вызова метода __str__() мы получим текст (строку) с заголовком записи.
    def __str__(self):
        return self.title_ru
