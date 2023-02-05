# Generated by Django 4.1.6 on 2023-02-04 17:03

from django.db import migrations
from django.db import models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name='Link',
            fields=[
                (
                    'id',
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name='ID',
                    ),
                ),
                ('original_url', models.URLField()),
                ('short_hash', models.CharField(max_length=6, unique=True)),
                ('views_counter', models.PositiveIntegerField(default=0)),
            ],
        ),
    ]
