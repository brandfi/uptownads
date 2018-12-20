from django.urls import path

from . import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.index, name='index'),
    path('impression-list/<str:title>/',
         views.impression_list, name='impression-list'),
    path('impressions/',
         views.impressions, name='impressions'),
    path('clicks/',
         views.clicks, name='clicks'),
    path('impressions-api/',
         views.impressions_api, name='impressions-api'),
    path('graphs/',
         views.graphs, name='graphs'),
]
