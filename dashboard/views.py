from django.shortcuts import render
from ads.models import Impression, Click, Ad
from django.db.models import Max
from datetime import date
import datetime

# Create your views here.


def index(request):
    impressions_count = Impression.objects.count()
    click_count = Click.objects.count()
    ad_list = Ad.objects.all()
    impression_max = Impression.objects.all().aggregate(Max('venue'))
    click_max = Click.objects.all().aggregate(Max('venue'))

    context = {
        'impressions_count': impressions_count,
        'click_count': click_count,
        'ad_list': ad_list,
        'venue_max': impression_max.get('venue__max'),
        'click_max': click_max.get('venue__max'),
    }
    return render(request, 'dashboard/index.html', context)


def impression_list(request, title):
    impression_list = Impression.objects.filter(ad__title=title)

    context = {
        'impression_list': impression_list,
    }
    return render(request, 'dashboard/impression-list.html', context)
