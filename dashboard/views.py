from django.shortcuts import render
from ads.models import Impression, Click, Ad

# Create your views here.


def index(request):
    impressions_count = Impression.objects.count()
    click_count = Click.objects.count()
    ad_list = Ad.objects.all()

    context = {
        'impressions_count': impressions_count,
        'click_count': click_count,
        'ad_list': ad_list,
    }
    return render(request, 'dashboard/index.html', context)


def impression_list(request, title):
    impression_list = Impression.objects.filter(ad__title=title)

    context = {
        'impression_list': impression_list,
    }
    return render(request, 'dashboard/impression-list.html', context)
