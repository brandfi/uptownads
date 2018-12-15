from django.urls import path

from . import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.index, name='index'),
    path('impression-list/<str:title>/',
         views.impression_list, name='impression-list'),
]
