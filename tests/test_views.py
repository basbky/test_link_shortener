import pytest

from model_mommy import mommy

from shortener.forms import URLShortenerForm
from shortener.models import Link
from shortener.views import RedirectView
from shortener.views import StatisticsView
from shortener.views import URLShortenerView


@pytest.mark.django_db
def test_url_shortener_view_form_valid():
    form = mommy.prepare(URLShortenerForm, url='http://www.example.com')
    request = mommy.prepare(
        type='django.http.HttpRequest',
        method='POST',
        POST={'url': 'http://www.example.com'},
    )
    view = URLShortenerView.as_view()

    response = view(request, form=form)

    assert response.status_code == 200
    assert 'short_hash' in response.context_data


@pytest.mark.django_db
def test_redirect_view_get():
    link = mommy.make(Link, original_url='http://www.example.com')
    request = mommy.prepare(type='django.http.HttpRequest', method='GET')
    view = RedirectView.as_view()

    response = view(request, short_hash=link.short_hash)

    assert response.status_code == 302
    assert response['location'] == 'http://www.example.com'
    assert link.views_counter == 1


@pytest.mark.django_db
def test_statistics_view_get():
    mommy.make(Link, _quantity=10)
    request = mommy.prepare(type='django.http.HttpRequest', method='GET')
    view = StatisticsView.as_view()

    response = view(request)

    assert response.status_code == 200
    assert 'links' in response.context_data
    assert len(response.context_data['links']) == 10
