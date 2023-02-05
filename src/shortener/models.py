from django.db import models


class Link(models.Model):
    original_url = models.URLField()
    short_hash = models.CharField(max_length=6, unique=True)
    views_counter = models.PositiveIntegerField(default=0)

    def increment_views_counter(self):
        self.views_counter += 1
        self.save()
