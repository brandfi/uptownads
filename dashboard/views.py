from django.shortcuts import render
from ads.models import Impression, Click, Ad
from django.db.models import Max
from django.db.models import Count
from django.http import JsonResponse

import json

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
    return render(request, 'dashboard/index.html', context)


def impression_list(request, title):
    impression_list = Impression.objects.filter(
        ad__title=title).order_by('-impression_date')

    context = {
        'impression_list': impression_list,
    }
    return render(request, 'dashboard/impression-list.html', context)


def impressions(request):
    impressions = Impression.objects.all().order_by('-impression_date')

    context = {
        'impressions': impressions,
    }
    return render(request, 'dashboard/impressions.html', context)


def clicks(request):
    clicks = Click.objects.all().order_by('-click_date')

    context = {
        'clicks': clicks,
    }
    return render(request, 'dashboard/clicks.html', context)


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


def graphs(request):
    return render(request, 'dashboard/graphs.html')
