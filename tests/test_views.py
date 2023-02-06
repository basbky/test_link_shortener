import pytest

from django.http import HttpResponse
from django.test import Client
from django.test import RequestFactory
from django.test import TestCase
from django.urls import reverse

from shortener.forms import URLShortenerForm
from shortener.models import Link
from shortener.views import StatisticsView


class URLShortenerViewTestCase(TestCase):
    def setUp(self):
        """
        Создает среду для выполнения тестов
        """
        self.client = Client()

    def test_form_valid(self):
        """
        Тестирует валидацию формы
        """
        form_data = {'url': 'https://www.example.com/'}
        request = self.client.post(
            reverse('url_shortener:url_shortener'), form_data
        )
        self.assertEqual(request.status_code, 200)
        self.assertTemplateUsed(request, 'shortener/url_shortener.html')

    def test_form_invalid(self):
        """
        Тестирует валидацию заведомо неподходящих вводных данных
        """
        form_data = {'url': ''}
        form = URLShortenerForm(data=form_data)
        self.assertFalse(form.is_valid())

        client = Client()
        response = client.post(
            reverse('url_shortener:url_shortener'), form_data
        )
        self.assertEqual(response.status_code, 200)


class RedirectViewTestCase(TestCase):
    def setUp(self):
        """
        Создает среду для выполнения тестов
        """
        self.link = Link.objects.create(
            original_url='https://example.com', short_hash='abcdef'
        )

    def test_redirect_view(self):
        """
        Тестирует переадресацию с короткой ссылки на оригинальную
        """
        response = self.client.get(
            reverse('url_shortener:redirect', args=['abcdef'])
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['location'], 'https://example.com')


@pytest.mark.django_db
class TestStatisticsView:
    def test_get_request(self):
        """
        Тестирует GET запрос
        """
        request = RequestFactory().get('/statistics/')
        response = StatisticsView.as_view()(request)

        assert response.status_code == 200
        assert isinstance(response, HttpResponse)

    def test_download_csv(self):
        """
        Тестирует возможность выгрузить статистику в формате .csv
        """
        request = RequestFactory().get('/statistics/?download_csv=True')
        response = StatisticsView.as_view()(request)

        assert response.status_code == 200
        assert isinstance(response, HttpResponse)
        assert (
            response['Content-Disposition']
            == 'attachment; filename="statistics.csv"'
        )
        assert response['Content-Type'] == 'text/csv'

    def test_download_xlsx(self):
        """
        Тестирует возможность выгрузить статистику в формате .xlsx
        """
        request = RequestFactory().get('/statistics/?download_xlsx=True')
        response = StatisticsView.as_view()(request)

        assert response.status_code == 200
        assert isinstance(response, HttpResponse)
        assert (
            response['Content-Disposition']
            == 'attachment; filename="statistics.xlsx"'
        )
        assert (
            response['Content-Type']
            == 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
