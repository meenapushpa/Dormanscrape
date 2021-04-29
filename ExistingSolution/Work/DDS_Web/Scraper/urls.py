from django.urls import path
from django.views.generic import RedirectView

from . import views

urlpatterns = [
    path('favicon.ico', RedirectView.as_view(url='/static/img/favicon.ico')),

    # path('', views.home,name='home'),
    path('', views.ScraperView.as_view(), name='home'),

    path('get_status', views.get_status, name='get_status'),
    path('stop_search', views.stop_search, name='stop_search'),
    path('save_userinfo', views.save_userinfo, name='save_userinfo'),
]
