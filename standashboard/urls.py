from django.urls import path

from . import views

app_name = 'standashboard'

urlpatterns = [
    path('', views.index, name='index'),
    path('impression-list/<str:title>/',
         views.impression_list, name='impression-list'),
    path('click-list/<str:title>/',
         views.click_list, name='click-list'),
    path('impressions/',
         views.impressions, name='impressions'),
    path('clicks/',
         views.clicks, name='clicks'),
    path('venues/',
         views.venues, name='venues'),
    path('click-venues/',
         views.click_venues, name='click-venues'),
    path('impressions-api/',
         views.impressions_api, name='impressions-api'),
    path('venues-api/',
         views.venues_api, name='venues-api'),
    path('clicks-api/',
         views.click_api, name='clicks-api'),
    path('total-clicks-api/',
         views.clicks_api),
    path('users-api/',
         views.users_api, name='users-api'),
    path('users/',
         views.users, name='users'),
    path('ad-datetime/api/<str:title>/',
         views.ad_datetime, name='ad-datetime'),
    path('clickad-datetime/api/<str:title>/',
         views.click_addatetime),
    path('venue-datetime/api/<str:venue_name>/',
         views.venue_datetime, name='venue-datetime'),
    path('click-datetime/api/<str:venue_name>/',
         views.click_datetime, name='click-datetime'),
    path('total-impressions-datetime/api/',
         views.total_impressions_datetime, name='total-impressions-datetime'),
    path('total-clicks-datetime/api/',
         views.total_clicks_datetime, name='total-clicks-datetime'),
]
