from django.shortcuts import render
from ads.models import Impression, Click, Ad, Venue
from django.db.models import Max
from django.db.models import Count
from django.http import JsonResponse
from collections import Counter

import json
import requests
# Create your views here.


def index(request):
    impressions_count = Impression.objects.count()
    click_count = Click.objects.count()
    ad_list = Ad.objects.annotate(
        no_of_impressions=Count('impressions'))
    ad_click_list = Ad.objects.annotate(
        no_of_impressions=Count('clicks'))
    impression_max = Impression.objects.all().values('venue').annotate(
        total=Count('venue')).order_by('-total')
    click_max = Click.objects.all().values('venue').annotate(
        total=Count('venue')).order_by('-total')

    context = {
        'impressions_count': impressions_count,
        'click_count': click_count,
        'ad_list': ad_list,
        'ad_click_list': ad_click_list,
        'venue_max': impression_max,
        'click_max': click_max,
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


def click_list(request, title):
    click_list = Click.objects.filter(
        ad__title=title).order_by('-click_date')

    context = {
        'click_list': click_list,
        'title': title,
    }
    return render(request, 'standashboard/click-list.html', context)


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


def venues(request):
    top_venue = Impression.objects.all().values('venue').annotate(
        total=Count('venue')).order_by('-total')
    context = {
        'top_venue': top_venue,
    }
    return render(request, 'standashboard/venues.html', context)


def click_venues(request):
    top_click = Click.objects.all().values('venue').annotate(
        total=Count('venue')).order_by('-total')
    context = {
        'top_click': top_click,
    }
    return render(request, 'standashboard/click_venue.html', context)


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


def clicks_api(request):
    ads = Ad.objects.annotate(
        no_of_impressions=Count('clicks'))

    data = []
    for ad in ads:
        item = {"title": ad.title}
        item["count"] = ad.no_of_impressions
        data.append(item)

    jsonData = json.dumps(data)
    return JsonResponse(jsonData, safe=False)


def venues_api(request):
    top_venue = Impression.objects.all().values('venue').annotate(
        total=Count('venue')).order_by('-total')

    data = []
    for v in top_venue:
        item = {"title": v['venue']}
        item["count"] = v['total']
        data.append(item)

    jsonData = json.dumps(data)
    return JsonResponse(jsonData, safe=False)


def click_api(request):
    top_venue = Click.objects.all().values('venue').annotate(
        total=Count('venue')).order_by('-total')

    data = []
    for v in top_venue:
        item = {"title": v['venue']}
        item["count"] = v['total']
        data.append(item)

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


def click_addatetime(request, title):
    graph_data = Click.objects.filter(ad__title=title).extra(
        {
            'date_created': "date(click_date)"
        }).values('date_created').annotate(
            created_count=Count('click_date')).order_by("date_created")

    data_list = []
    for data in graph_data:
        item = {
            "impression_date": "{:%m/%d/%Y}".format(data.get('date_created'))}
        item["count"] = data.get('created_count')
        data_list.append(item)

    jsonData = json.dumps(data_list)
    return JsonResponse(jsonData, safe=False)


def venue_datetime(request, venue_name):
    venue_data = Impression.objects.filter(venue=venue_name).extra(
        {
            'date_created': "date(impression_date)"
        }).values('date_created').annotate(
            created_count=Count('impression_date')).order_by("date_created")

    data_list = []
    for data in venue_data:
        item = {
            "impression_date": "{:%m/%d/%Y}".format(data.get('date_created'))}
        item["count"] = data.get('created_count')
        data_list.append(item)

    jsonData = json.dumps(data_list)
    return JsonResponse(jsonData, safe=False)


def click_datetime(request, venue_name):
    click_data = Click.objects.filter(venue=venue_name).extra(
        {
            'date_created': "date(click_date)"
        }).values('date_created').annotate(
            created_count=Count('click_date')).order_by("date_created")

    data_list = []
    for data in click_data:
        item = {
            "impression_date": "{:%m/%d/%Y}".format(data.get('date_created'))}
        item["count"] = data.get('created_count')
        data_list.append(item)

    jsonData = json.dumps(data_list)
    return JsonResponse(jsonData, safe=False)


def total_impressions_datetime(request):
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


def total_impressions_datetime(request):
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


def total_clicks_datetime(request):
    clicks_data = Click.objects.extra(
        {
            'date_created': "date(click_date)"
        }).values('date_created').annotate(
            created_count=Count('click_date')).order_by("date_created")

    data_list = []
    for data in clicks_data:
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


def users_api(request):
    headers = {'Content-type': 'application/json'}
    r = requests.get(
        'http://radiusapi.brandfi.co.ke/radiusapi/users/', headers=headers)

    users = r.json()
    filtered_users = [user for user in users if user['ssid'] == 'uptownsms'
                      or user['ssid'] == 'kahawasms'
                      or user['ssid'] == 'saapesms'
                      or user['ssid'] == 'taylorgraysms']
    u = Counter(user['ssid'] for user in filtered_users)
    return JsonResponse(u, safe=False)


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
