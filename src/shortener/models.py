from django.db import models


class Link(models.Model):
    original_url = models.URLField('Оригинальная ссылка')
    short_hash = models.CharField(
        'Хеш ссылки', max_length=6, unique=True, db_index=True
    )
    views_count = models.PositiveIntegerField(
        'Счётчик переходов по ссылке', default=0
    )

    def __str__(self):
        return self.original_url

    class Meta:
        verbose_name = 'Ссылка'
        verbose_name_plural = 'Ссылки'
