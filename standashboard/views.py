from django.shortcuts import render
from ads.models import Impression, Click, Ad, Venue
from django.db.models import Max
from django.db.models import Count
from django.http import JsonResponse

import json
import requests
# Create your views here.


def index(request):
    impressions_count = Impression.objects.count()
    click_count = Click.objects.count()
    ad_list = Ad.objects.annotate(
        no_of_impressions=Count('impressions'))
    impression_max = Impression.objects.all().aggregate(Max('venue'))

    context = {
        'impressions_count': impressions_count,
        'click_count': click_count,
        'ad_list': ad_list,
        'venue_max': impression_max.get('venue__max'),
    }
    return render(request, 'standashboard/index.html', context)


def impression_list(request, title):
    impression_list = Impression.objects.filter(
        ad__title=title).order_by('-impression_date')

    context = {
        'impression_list': impression_list,
        'title': title,
    }
    return render(request, 'standashboard/impression-list.html', context)


def impressions(request):
    impressions = Impression.objects.all().order_by('-impression_date')

    context = {
        'impressions': impressions,
    }
    return render(request, 'standashboard/impressions.html', context)


def total_impressions(request):
    impressions_data = Impression.objects.extra(
        {
            'date_created': "date(impression_date)"
        }).values('date_created').annotate(
            created_count=Count('impression_date')).order_by("date_created")

    data_list = []
    for data in impressions_data:
        item = {
            "impression_date": "{:%m/%d/%Y}".format(data.get('date_created'))}
        item["count"] = data.get('created_count')
        data_list.append(item)

    jsonData = json.dumps(data_list)
    return JsonResponse(jsonData, safe=False)


def clicks(request):
    clicks = Click.objects.all().order_by('-click_date')

    context = {
        'clicks': clicks,
    }
    return render(request, 'standashboard/clicks.html', context)


def impressions_api(request):
    ads = Ad.objects.annotate(
        no_of_impressions=Count('impressions'))

    data = []
    for ad in ads:
        item = {"title": ad.title}
        item["count"] = ad.no_of_impressions
        data.append(item)

    jsonData = json.dumps(data)
    return JsonResponse(jsonData, safe=False)


def venues_api(request):
    venues = Venue
    ads = Ad.objects.annotate(
        no_of_venues=Count('venues'))

    data = []
    for ad in ads:
        print(ad.no_of_venues)

    jsonData = json.dumps(data)
    return JsonResponse(jsonData, safe=False)


def ad_datetime(request, title):
    graph_data = Impression.objects.filter(ad__title=title).extra(
        {
            'date_created': "date(impression_date)"
        }).values('date_created').annotate(
            created_count=Count('impression_date')).order_by("date_created")

    data_list = []
    for data in graph_data:
        item = {
            "impression_date": "{:%m/%d/%Y}".format(data.get('date_created'))}
        item["count"] = data.get('created_count')
        data_list.append(item)

    jsonData = json.dumps(data_list)
    return JsonResponse(jsonData, safe=False)


def users(request):
    headers = {'Content-type': 'application/json'}
    r = requests.get(
        'http://radiusapi.brandfi.co.ke/radiusapi/users/', headers=headers)

    users = r.json()
    filtered_users = [user for user in users if user['ssid'] == 'uptownsms'
                      or user['ssid'] == 'kahawasms'
                      or user['ssid'] == 'saapesms'
                      or user['ssid'] == 'taylorgraysms']

    for user in filtered_users:
        print(user['ssid'])
    context = {
        'filtered_users': filtered_users,
    }
    return render(request, 'standashboard/users.html', context)


def events_api(request):
    json_string = '''{
            "title": "Saape",
            "count": 968
        },
        {
            "title": "Uptown",
            "count": 689
        },
        {
            "title": "Kahawa",
            "Freq": 329
        },
        {
            "Letter": "Taylor",
            "Freq": 404
        }|'''
    event_json = json.dumps(json_string)
    return JsonResponse(json_string, safe=False)
