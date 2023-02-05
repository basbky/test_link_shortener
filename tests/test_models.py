import pytest

from django.urls import reverse

from shortener.models import Link


@pytest.mark.django_db
def test_link_model():
    link = Link.objects.create(
        original_url="https://www.example.com", short_hash="abcdef"
    )

    # Проверяет, создан ли объект
    assert link.pk is not None

    # Проверяет дефолтное значение views_counter
    assert link.views_counter == 0

    # Проверяет работоспособность метода класса increment_views_counter
    link.increment_views_counter()
    assert link.views_counter == 1
