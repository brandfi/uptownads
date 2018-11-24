# Create your views here.
from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from splashads.generate import TOTPVerification

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
        reverse('saape:check-credentials')

    context = {
        'url': url,
    }

    return render(request, 'saape/index.html', context)


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
            reverse('saape:success')
        login_params = {"username": user['username'],
                        "password": user['value'],
                        "success_url": successs_url}
        r = requests.post(login_url, params=login_params)
        return HttpResponseRedirect(r.url)
    else:
        return HttpResponseRedirect(reverse('saape:signup'))


@csrf_exempt
def signup(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        phone_number = request.POST['phone_number']
        client_mac = request.session['client_mac']
        generated_token = totp_verification.generate_token()

        ssid = 'saapesms'
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
        return HttpResponseRedirect(reverse('saape:verify'))

    terms_url = 'http://' + request.get_host() + \
        reverse('saape:terms')

    context = {
        'terms_url': terms_url,
    }
    return render(request, 'saape/signup.html', context)


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
                    reverse('saape:success')
                login_params = {"username": user['username'],
                                "password": user['value'],
                                "success_url": successs_url}
                r = requests.post(login_url, params=login_params)
                return HttpResponseRedirect(r.url)
            else:
                status = 'error'
        else:
            status = 'error'

    context = {
        'message': status,
    }
    return render(request, 'saape/verify.html', context)


def success(request):
    return render(request, 'saape/success.html')


def terms(request):
    return render(request, 'saape/terms.html')
