from django.urls import path

from . import views

app_name = 'adtest'

urlpatterns = [
    path('', views.index, name='index'),
    path('home', views.home, name='home'),
    path('login', views.login, name='login'),
    path('success', views.success, name='success'),
    path('terms', views.terms, name='terms'),
]
