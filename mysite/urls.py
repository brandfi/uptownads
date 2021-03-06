"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.contrib import admin


# Admin Site Config
admin.sites.AdminSite.site_header = 'Brandfi'
admin.sites.AdminSite.site_title = 'Brandfi Ad Manager'
admin.site.site_url = 'http://adm.brandfi.co.ke/admin'

urlpatterns = [
    path('ads/', include('ads.urls')),
    path('splashads/', include('splashads.urls')),
    path('saape/', include('saape.urls')),
    path('saapetrm/', include('saapetrm.urls')),
    path('hacienda/', include('hacienda.urls')),
    path('scotchies/', include('scotchies.urls')),
    path('brewbistro/', include('brewbistro.urls')),
    path('taylorgray/', include('taylorgray.urls')),
    path('kahawa/', include('kahawa.urls')),
    path('standashboard/', include('standashboard.urls')),
    path('adtest/', include('adtest.urls')),
    path('admin/', admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
