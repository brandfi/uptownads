from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect

from django.conf import settings
from django.utils import timezone

from ads.models import Ad, Impression
from ads.utils import get_client_ip
from django.shortcuts import redirect
# Create your views here.


def index(request):
    base_grant_url = request.GET.get('base_grant_url', '')
    user_continue_url = request.GET.get('user_continue_url', '')
    node_id = request.GET.get('node_id', '')
    node_mac = request.GET.get('node_mac', '')
    gateway_id = request.GET.get('gateway_id', '')
    client_ip = request.GET.get('client_ip', '')
    client_mac = request.GET.get('client_mac', '')

    request.session['base_grant_url'] = base_grant_url
    request.session['user_continue_url'] = user_continue_url
    request.session['node_id'] = node_id
    request.session['node_mac'] = node_mac
    request.session['gateway_id'] = gateway_id
    request.session['client_ip'] = client_ip
    request.session['client_mac'] = client_mac

    url = 'http://' + request.get_host() + \
        reverse('adtest:home')

    # Retrieve random ad for the zone based on weight
    ad = Ad.objects.random_ad('header', 'Uptown')

    if ad is not None:
        if request.session.session_key:
            impression, created = Impression.objects.get_or_create(
                ad=ad,
                session_id=request.session.session_key,
                defaults={
                    'impression_date': timezone.now(),
                    'source_ip': get_client_ip(request),
                    'venue': 'Uptown',
                    'url': 'Uptown Landing Page',
                })

    context = {
        'url': url,
        'ad': ad,
        'zone': settings.ADS_ZONES.get('header', None),
    }

    return render(request, 'adtest/index.html', context)


def home(request):
    terms_url = 'http://' + request.get_host() + \
        reverse('adtest:terms')
    home_url = 'http://' + request.get_host() + \
        reverse('adtest:home')
    login_url = 'http://' + request.get_host() + \
        reverse('adtest:login')

    context = {
        'terms_url': terms_url,
        'home_url': home_url,
        'login_url': login_url,
    }
    return render(request, 'adtest/home.html', context)


def login(request):
    continue_url = 'http://' + request.get_host() + \
        reverse('adtest:success')
    base_grant_url = request.session['base_grant_url']
    redirect_url = base_grant_url + '/?continue_url=' + continue_url
    return redirect(redirect_url)


def success(request):
    success_url = 'http://' + request.get_host() + \
        reverse('adtest:success')

    context = {
        'success_url': success_url,

    }
    return render(request, 'adtest/success.html', context)


def terms(request):
    return render(request, 'adtest/terms.html')
