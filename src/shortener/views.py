from django.http import HttpResponse
from django.shortcuts import redirect
from django.shortcuts import render
from django.views import View
from django.views.generic import FormView
from django.views.generic import TemplateView

from .forms import URLShortenerForm
from .models import Link
from .utils import create_csv_file
from .utils import create_xlsx_file
from .utils import get_paginated_links
from .utils import get_sorted_links
from .utils import save_url_mapping


class URLShortenerView(FormView):
    """
    URLShortenerView обеспечивает функционал сократителя ссылок
    Обеспечивает рендер формы и принятия данных, внесенных в нее
    """

    template_name = 'shortener/url_shortener.html'
    form_class = URLShortenerForm

    def form_valid(self, form: URLShortenerForm):
        """
        Метод вызывается при валидной передаче данных в форму
        Он сокращает оригинальную ссылку и передает новый хеш ссылки

        :param form: Данные из формы
        :type form: URLShortenerForm
        :return: Рендерит ответ с хешем ссылки
        :rtype: HttpResponse
        """
        url = form.cleaned_data['url']
        short_hash = save_url_mapping(url)
        context = {'short_hash': short_hash}
        return render(self.request, 'shortener/url_shortener.html', context)


class RedirectView(View):
    """
    RedirectView обеспечивает функционал перенаправления пользователя с сокращенной ссыллки на оригинальную.
    """

    def get(self, request, short_hash: str):
        """
        Метод вызывается при запросе GET
        Он увеличивает количество переходов на 1 и перенаправляет на оригинальный url

        :param request: Django request object
        :type request: HttpRequest
        :param short_hash: Хеш оригинальной ссылки
        :type short_hash: str
        :return: Перенаправляет на оригинальную ссылку
        :rtype: HttpResponseRedirect
        """
        mapping = Link.objects.get(short_hash=short_hash)
        mapping.increment_views_counter()
        return redirect(mapping.original_url)


class StatisticsView(TemplateView):
    """
    Выводит статистику по всем сокращенным ссылкам и количествами переходов по ним
    """

    template_name = 'shortener/statistics.html'

    def get(self, request, *args, **kwargs):
        """
        Обрабатывает GET запрос для вывода статистики

        Статистика сортируется по query string параметру sort_by, по-умолчанию стоит 'views_counter'
        Обработанные данные проходят пагинацию и выводятся на страницу

        Если в GET запросе передан параметр download_csv, то статистика выгружается в .csv файле
        Если в GET запросе передан параметр download_xlsx, то статистика выгружается в .xlsx файле

        :param request: входящий request object
        :type request: django.http.HttpRequest
        :param args: дополнительные аргументы
        :type args: list
        :param kwargs: дополнительные ключевые аргументы
        :type kwargs: dict
        :return: ответ на запрос
        :rtype: django.http.HttpResponse
        """
        # Сортирует данные на основе sort_by параметра, по-умолчанию стоит 'views_counter'
        sort_by = request.GET.get('sort_by', 'views_counter')
        links = get_sorted_links(sort_by)

        # Если в GET запросе передан параметр download_csv, то статистика выгружается в .csv файле
        if request.GET.get('download_csv'):
            create_csv_file(links)
            file = open('statistics.csv', 'r')
            response = HttpResponse(file, content_type='text/csv')
            response[
                'Content-Disposition'
            ] = 'attachment; filename="statistics.csv"'
            return response
        # Если в GET запросе передан параметр download_xlsx, то статистика выгружается в .xlsx файле
        elif request.GET.get('download_xlsx'):
            create_xlsx_file(links)
            file = open('statistics.xlsx', 'rb')
            response = HttpResponse(
                file.read(),
                content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            )
            response[
                'Content-Disposition'
            ] = 'attachment; filename="statistics.xlsx"'
            return response

        # Получает количество страниц для вывода на сайте, по-умолчанию стоит значение 1
        page = request.GET.get('page', 1)

        # Пагинирует ссылки
        links = get_paginated_links(links, page_number=page)

        # Обновляет context ссылками, прошедшими пагинацию
        context = self.get_context_data(**kwargs)
        context['links'] = links

        # Отправка ответа

        return self.render_to_response(context)
