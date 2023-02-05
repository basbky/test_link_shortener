from django.core.paginator import Paginator
from django.shortcuts import redirect
from django.shortcuts import render
from django.urls import reverse
from django.views import View
from django.views.generic import FormView
from django.views.generic import TemplateView

from .forms import URLShortenerForm
from .models import Link
from .utils import generate_short_hash
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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        sort_by = (
            self.request.GET.get('sort_by', 'views_counter') or 'views_counter'
        )
        links = Link.objects.all().order_by(sort_by)

        paginator = Paginator(links, 10)
        page = self.request.GET.get('page')
        links = paginator.get_page(page)

        context['links'] = links
        return context
