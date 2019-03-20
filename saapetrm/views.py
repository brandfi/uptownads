# Create your views here.
from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from splashads.generate import TOTPVerification

from django.conf import settings
from django.utils import timezone

from ads.models import Ad, Impression
from ads.utils import get_client_ip

import requests
import json

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
        reverse('saapetrm:check-credentials')

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
                    'venue': 'Saapetrm',
                    'url': 'Saape Landing Page',
                })

    context = {
        'url': url,
        'ad': ad,
        'zone': settings.ADS_ZONES.get('header', None),
    }

    return render(request, 'saapetrm/index.html', context)


def check_credentials(request):
    client_mac = request.session['client_mac']
    ssid = 'saapesms'
    headers = {'Content-type': 'application/json'}
    r = requests.get(
        'http://radiusapi.brandfi.co.ke/radiusapi/user-detail/' +
        client_mac + '/' + ssid, headers=headers)

    if r.status_code == 200:
        user = r.json()
        login_url = request.session['login_url']
        successs_url = 'http://' + request.get_host() + \
            reverse('saapetrm:success')
        login_params = {"username": user['username'],
                        "password": user['value'],
                        "success_url": successs_url}
        r = requests.post(login_url, params=login_params)
        return HttpResponseRedirect(r.url)
    else:
        return HttpResponseRedirect(reverse('saapetrm:signup'))


@csrf_exempt
def signup(request):
    if request.method == 'POST':
        phone_number = request.POST['phone_number']
        client_mac = request.session['client_mac']
        generated_token = totp_verification.generate_token()

        ssid = 'saapesms'
        username = phone_number + client_mac + ssid
        request.session['uname'] = username
        request.session['g_token'] = generated_token
        # Create a user

        user = {
            "username": username,
            "macAddress": client_mac,
            "mobileNumber": phone_number,
            "name": "NULL",
            "email": "NULL",
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
        return HttpResponseRedirect(reverse('saapetrm:verify'))

    terms_url = 'http://' + request.get_host() + \
        reverse('saapetrm:terms')

    context = {
        'terms_url': terms_url,
    }
    return render(request, 'saapetrm/signup.html', context)


@csrf_exempt
def verify(request):
    status = ''
    if request.method == 'POST':
        password = request.POST['password']
        headers = {'Content-type': 'application/json'}

        client_mac = request.session['client_mac']
        ssid = 'saapesms'
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
                    reverse('saapetrm:success')
                login_params = {"username": user['username'],
                                "password": user['value']
                                }
                # r = requests.post(login_url, params=login_params)
                # return HttpResponseRedirect(r.url)
                return JsonResponse(login_params) 
            else:
                status = 'error'
        else:
            status = 'error'
          
    context = {
        'message': status,
        'uname': request.session['uname'],
        'l_url': request.session['login_url'],
        'g_token': request.session['g_token'],
        'dst': 'http://' + request.get_host() + \
                    reverse('saapetrm:success')
    }
    return render(request, 'saapetrm/verify.html', context)


def success(request):
    return render(request, 'saapetrm/success.html')


def terms(request):
    return render(request, 'saapetrm/terms.html')
