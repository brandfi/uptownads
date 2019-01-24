from django.urls import path

from . import views

app_name = 'ads'

urlpatterns = [
    path('<int:pk>/<str:venue>/',
         views.AdClickView.as_view(), name='ad-click'),
    path('users/', views.get_users, name='get-users'),
]
