import pytest

from django.conf import settings

from shortener.models import Link


@pytest.fixture(scope='session')
def db_host_fixture(request):
    original_db_host = settings.DATABASES["default"]["HOST"]
    settings.DATABASES["default"]["HOST"] = "localhost"

    def reset_db_host():
        settings.DATABASES["default"]["HOST"] = original_db_host

    request.addfinalizer(reset_db_host)


@pytest.mark.django_db
def test_link_model(db_host_fixture):
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
