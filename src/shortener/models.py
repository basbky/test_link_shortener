from django.db import models


class Link(models.Model):
    """
    Модель, представляющая сокращенную ссылку
    """

    original_url = models.URLField()
    short_hash = models.CharField(max_length=6, unique=True)
    views_counter = models.PositiveIntegerField(default=0)

    def increment_views_counter(self) -> None:
        """
        Увеличивает количество переходов для определенной ссылки
        """
        self.views_counter += 1
        self.save()
