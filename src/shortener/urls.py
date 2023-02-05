from django.urls import path

from .views import RedirectView
from .views import StatisticsView
from .views import URLShortenerView


app_name = 'url_shortener'

urlpatterns = [
    path('', URLShortenerView.as_view(), name='url_shortener'),
    path('r/<str:short_hash>/', RedirectView.as_view(), name='redirect'),
    path('statistics/', StatisticsView.as_view(), name='statistics'),
]
