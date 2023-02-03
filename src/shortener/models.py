import base64
import os
import uuid

from django.db import models
from dotenv import find_dotenv
from dotenv import load_dotenv


load_dotenv(find_dotenv())

HOST_NAME = os.getenv('HOST_NAME', default='https://localhost:8000/')


class Link(models.Model):
    url = models.URLField('Ссылка')
    url_hash = models.CharField(
        'Хеш ссылки', max_length=6, unique=True, db_index=True
    )
    created_at = models.DateTimeField('Время создания', auto_now_add=True)
    views_counter = models.PositiveBigIntegerField(
        'Счётчик переходов', default=0
    )

    def __str__(self):
        return f'{self.url} to {self.url_hash}'

    def save(self, *args, **kwargs):
        self.url_hash = self.generate_hash()
        self.short_url = self.create_short_url()
        super(Link, self).save(*args, **kwargs)

    def generate_hash(self):
        url_hash = base64.urlsafe_b64encode(uuid.uuid1().bytes)[:6]
        hash_exist = Link.objects.filter(url_hash=url_hash)
        while hash_exist:
            url_hash = base64.urlsafe_b64encode(uuid.uuid1().bytes)[:6]
            hash_exist = Link.objects.filter(url_hash=url_hash)
            continue
        url_hash = url_hash.decode('utf-8')

        return url_hash

    def create_short_url(self):
        return HOST_NAME + self.url_hash

    class Meta:
        verbose_name = 'Ссылка'
        verbose_name_plural = 'Ссылки'
