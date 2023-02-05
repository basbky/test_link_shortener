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
    template_name = 'shortener/url_shortener.html'
    form_class = URLShortenerForm

    def form_valid(self, form):
        url = form.cleaned_data['url']
        short_hash = save_url_mapping(url)
        context = {'short_hash': short_hash}
        return render(self.request, 'shortener/url_shortener.html', context)


class RedirectView(View):
    def get(self, request, short_hash):
        mapping = Link.objects.get(short_hash=short_hash)
        mapping.increment_views_counter()
        return redirect(mapping.original_url)


class StatisticsView(TemplateView):
    template_name = 'shortener/statistics.html'

    def get(self, request, *args, **kwargs):
        sort_by = (
            request.GET.get('sort_by', 'views_counter') or 'views_counter'
        )
        links = get_sorted_links(sort_by)

        if request.GET.get('download_csv'):
            create_csv_file(links)
            file = open('statistics.csv', 'r')
            response = HttpResponse(file, content_type='text/csv')
            response[
                'Content-Disposition'
            ] = 'attachment; filename="statistics.csv"'
            return response
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

        page = request.GET.get('page')
        links = get_paginated_links(links, page_number=page)

        context = self.get_context_data(**kwargs)
        context['links'] = links
        return self.render_to_response(context)
