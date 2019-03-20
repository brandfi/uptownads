from django.urls import path

from saapetrm import views

app_name = 'saapetrm'

urlpatterns = [
    path('', views.index, name='index'),
    path('check-credentials',
         views.check_credentials,
         name='check-credentials'),
    path('signup', views.signup, name='signup'),
    path('verify', views.verify, name='verify'),
    path('success', views.success, name='success'),
    path('terms', views.terms, name='terms'),
]
