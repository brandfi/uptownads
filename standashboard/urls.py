from django.urls import path

from . import views

app_name = 'standashboard'

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
    path('venues-api/',
         views.venues_api, name='venues-api'),
    path('users/',
         views.users, name='users'),
    path('ad-datetime/api/<str:title>/',
         views.ad_datetime, name='ad-datetime'),
    path('total-impressions/api/',
         views.total_impressions, name='total-impressions'),
    path('total-events/api/',
         views.events_api, name='total-events'),
]
