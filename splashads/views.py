from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from splashads.generate import TOTPVerification

import requests
import json

from django.conf import settings
from django.utils import timezone

from ads.models import Ad, Impression
from ads.utils import get_client_ip

totp_verification = TOTPVerification()


def index(request):
    login_url = request.GET.get('login_url', '')
    continue_url = request.GET.get('continue_url', '')
    ap_name = request.GET.get('ap_name', '')
    ap_mac = request.GET.get('ap_mac', '')
    ap_tags = request.GET.get('ap_tags', '')
    client_ip = request.GET.get('client_ip', '')
    client_mac = request.GET.get('client_mac', '')

    request.session['login_url'] = login_url
    request.session['continue_url'] = continue_url
    request.session['ap_name'] = ap_name
    request.session['ap_mac'] = ap_mac
    request.session['ap_tags'] = ap_tags
    request.session['client_ip'] = client_ip
    request.session['client_mac'] = client_mac

    url = 'http://' + request.get_host() + \
        reverse('splashads:check-credentials')

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

    return render(request, 'splashads/index.html', context)


def check_credentials(request):
    client_mac = request.session['client_mac']
    ssid = 'uptownsms'
    headers = {'Content-type': 'application/json'}
    r = requests.get(
        'http://radiusapi.brandfi.co.ke/radiusapi/user-detail/' +
        client_mac + '/' + ssid, headers=headers)

    if r.status_code == 200:
        user = r.json()
        login_url = request.session['login_url']
        successs_url = 'http://' + request.get_host() + \
            reverse('splashads:success')
        login_params = {"username": user['username'],
                        "password": user['value'],
                        "success_url": successs_url}
        r = requests.post(login_url, params=login_params)
        return HttpResponseRedirect(r.url)
    else:
        return HttpResponseRedirect(reverse('splashads:signup'))


@csrf_exempt
def signup(request):
    if request.method == 'POST':
        name = request.POST['name']
        phone_number = request.POST['phone_number']
        client_mac = request.session['client_mac']
        generated_token = totp_verification.generate_token()

        ssid = 'uptownsms'
        username = phone_number + client_mac + ssid

        # Create a user

        user = {
            "username": username,
            "macAddress": client_mac,
            "mobileNumber": phone_number,
            "name": name,
            "email": email,
            "ssid": ssid,
            "attribute": "Cleartext-Password",
            "op": ":=",
            "value": generated_token
        }

        headers = {'Content-type': 'application/json'}
        r = requests.post(
            'http://radiusapi.brandfi.co.ke/radiusapi/create-user/',
            json=user,
            headers=headers)

        sms_url = 'http://pay.brandfi.co.ke:8301/sms/send'
        welcome_message = 'Online access code is: ' + generated_token
        sms_params = {
            "clientId": "2",
            "message": welcome_message,
            "recepients": phone_number
        }
        headers = {'Content-type': 'application/json'}
        sms_r = requests.post(
            sms_url,
            json=sms_params,
            headers=headers)
        return HttpResponseRedirect(reverse('splashads:verify'))

    terms_url = 'http://' + request.get_host() + \
        reverse('splashads:terms')
    signup_url = 'http://' + request.get_host() + \
        reverse('splashads:signup')

    context = {
        'terms_url': terms_url,
        'signup_url': signup_url,
    }
    return render(request, 'splashads/signup.html', context)


@csrf_exempt
def verify(request):
    status = ''
    if request.method == 'POST':
        password = request.POST['password']
        headers = {'Content-type': 'application/json'}

        client_mac = request.session['client_mac']
        ssid = 'uptownsms'
        headers = {'Content-type': 'application/json'}
        r = requests.get(
            'http://radiusapi.brandfi.co.ke/radiusapi/user-detail/' +
            client_mac + '/' + ssid, headers=headers)

        print(r.status_code)
        if r.status_code == 200:
            user = r.json()
            if user['value'] == password:
                login_url = request.session['login_url']
                successs_url = 'http://' + request.get_host() + \
                    reverse('splashads:success')
                login_params = {"username": user['username'],
                                "password": user['value'],
                                "success_url": successs_url}
                r = requests.post(login_url, params=login_params)
                return HttpResponseRedirect(r.url)
            else:
                status = 'error'
        else:
            status = 'error'

    verify_url = 'http://' + request.get_host() + \
        reverse('splashads:verify')
    context = {
        'message': status,
        'verify_url': verify_url,
    }
    return render(request, 'splashads/verify.html', context)


def success(request):
    success_url = 'http://' + request.get_host() + \
        reverse('splashads:success')

    context = {
        'success_url': success_url,

    }
    return render(request, 'splashads/success.html', context)


def terms(request):
    return render(request, 'splashads/terms.html')
