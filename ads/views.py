from django.http import HttpResponseRedirect
from django.conf import settings
from django.shortcuts import render
from django.views import View
from django.utils import timezone
from django.views.generic.detail import SingleObjectMixin

from ads.models import Ad, Click, Impression
from ads.serializers import ImpressionSerializer
from ads.utils import get_client_ip

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

import requests
import json


class AdClickView(SingleObjectMixin, View):
    def get_queryset(self):
        return Ad.objects.all()

    def get(self, request, *args, **kwargs):
        ad = self.get_object()
        click, created = Click.objects.get_or_create(
            ad=ad,
            session_id=request.session.session_key,
            defaults={
                'click_date': timezone.now(),
                'source_ip': get_client_ip(request),
                'venue': self.kwargs['venue'],
            })
        return HttpResponseRedirect(ad.url)


def get_users(request):
    headers = {'Content-type': 'application/json'}
    r = requests.get(
        'http://radiusapi.brandfi.co.ke/radiusapi/users/', headers=headers)

    users = r.json()
    filtered_users = [user for user in users if user['ssid'] == 'uptownsms'
                      or user['ssid'] == 'kahawasms'
                      or user['ssid'] == 'saapesms'
                      or user['ssid'] == 'taylorgraysms']
    context = {
        'filtered_users': filtered_users,
    }
    return render(request, 'ads/users.html', context)


@api_view(['GET'])
def impressions_list(request, title):
    """
    List all impressions.
    """
    impressions = Impression.objects.filter(ad__title=title)
    serializer = ImpressionSerializer(impressions, many=True)
    return Response(serializer.data)
