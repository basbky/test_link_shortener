import string

import pytest

from django.conf import settings


@pytest.fixture(scope='session')
def db_host_fixture(request):
    """
    Фикстура, обсепечивающая корректное взаимодействие тестов с мок-базой данных
    :param request: запрос, необходимый для выполнения теста
    """
    original_db_host = settings.DATABASES["default"]["HOST"]
    settings.DATABASES["default"]["HOST"] = "localhost"

    def reset_db_host():
        settings.DATABASES["default"]["HOST"] = original_db_host

    request.addfinalizer(reset_db_host)


def test_generate_short_hash():
    """
    Тестирует генерацию хеша ссылки
    :return:
    """
    from shortener.utils import generate_short_hash

    # Тестирует стандартную длину
    short_hash = generate_short_hash()
    assert len(short_hash) == 6
    assert all(c in string.ascii_letters + string.digits for c in short_hash)

    # Тестирует кастомную длину
    short_hash = generate_short_hash(length=8)
    assert len(short_hash) == 8
    assert all(c in string.ascii_letters + string.digits for c in short_hash)


@pytest.mark.django_db
def test_save_url_mapping(db_host_fixture):
    """
    Тестирует сохранение маппинга хешей к оригинальным ссылкам
    :param db_host_fixture: Фикстура для корректной работы тестов
    """
    from shortener.models import Link
    from shortener.utils import save_url_mapping

    # Тестирует различые варианты входных данных
    original_url = 'https://www.example.com/'
    short_hash = save_url_mapping(original_url)
    link = Link.objects.get(short_hash=short_hash)
    assert link.original_url == original_url

    original_url = 'https://www.example.org/'
    short_hash = save_url_mapping(original_url)
    link = Link.objects.get(short_hash=short_hash)
    assert link.original_url == original_url


@pytest.mark.django_db
def test_get_sorted_links(db_host_fixture):
    """
    Тестирует сортировку ссылок для дальнейшей пагинации
    """
    from shortener.models import Link
    from shortener.utils import get_sorted_links

    Link.objects.create(
        original_url='https://www.example.com/',
        views_counter=10,
        short_hash='abc123',
    )
    Link.objects.create(
        original_url='https://www.example.org/',
        views_counter=20,
        short_hash='def456',
    )
    Link.objects.create(
        original_url='https://www.example.net/',
        views_counter=5,
        short_hash='ghi789',
    )

    links = get_sorted_links()
    assert links[0].views_counter == 5
    assert links[1].views_counter == 10
    assert links[2].views_counter == 20

    links = get_sorted_links(sort_by='original_url')
    assert links[0].original_url == 'https://www.example.com/'
    assert links[1].original_url == 'https://www.example.net/'
    assert links[2].original_url == 'https://www.example.org/'


@pytest.mark.django_db
def test_get_paginated_links(db_host_fixture):
    """
    Тестирует пагинацию ссылок
    """
    from shortener.models import Link
    from shortener.utils import get_paginated_links

    Link.objects.create(
        original_url='https://www.example.com/',
        views_counter=10,
        short_hash='abc123',
    )
    Link.objects.create(
        original_url='https://www.example.org/',
        views_counter=20,
        short_hash='def456',
    )
    Link.objects.create(
        original_url='https://www.example.net/',
        views_counter=5,
        short_hash='ghi789',
    )
    Link.objects.create(
        original_url='https://www.example.info/',
        views_counter=15,
        short_hash='jkl012',
    )
    Link.objects.create(
        original_url='https://www.example.biz/',
        views_counter=25,
        short_hash='mno345',
    )

    links = Link.objects.all()
    page = get_paginated_links(links)
    assert len(page) <= 10
    assert page.has_previous() is False
    assert page.has_next() is False

    page = get_paginated_links(links, page_size=2, page_number=2)
    assert len(page) == 2
    assert page.has_previous() is True
    assert page.has_next() is True

    page = get_paginated_links(links, page_size=2, page_number=4)
    assert len(page) == 1
    assert page.has_previous() is True
    assert page.has_next() is False
