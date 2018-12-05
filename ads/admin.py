from __future__ import unicode_literals

from django import forms
from django.contrib import admin

from ads.forms import *
from ads.models import *

# Register your models here.


class AdvertiserAdmin(admin.ModelAdmin):
    search_fields = ['company_name', 'website']
    list_display = ['company_name', 'website', 'created_by']
    raw_id_fields = ['created_by']

    def get_changeform_initial_data(self, request):
        """
        Provide initial datas when creating an advertiser.
        """
        get_data = super(
            AdvertiserAdmin, self).get_changeform_initial_data(request)
        return get_data or {
            'created_by': request.user.pk
        }


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['title', 'created_by']
    raw_id_fields = ['created_by']

    def get_changeform_initial_data(self, request):
        """
        Provide initial datas when creating a category.
        """
        get_data = super(CategoryAdmin, self). \
            get_changeform_initial_data(request)
        return get_data or {
            'created_by': request.user.pk
        }


class VenueAdmin(admin.ModelAdmin):
    form = VenueForm
    list_display = ['title', 'location', 'group', 'created_by']
    raw_id_fields = ['created_by']

    def get_changeform_initial_data(self, request):
        """
        Provide initial datas when creating a category.
        """
        get_data = super(VenueAdmin, self). \
            get_changeform_initial_data(request)
        return get_data or {
            'created_by': request.user.pk
        }


class AdImageInline(admin.TabularInline):
    model = AdImage
    form = AdImageInlineForm
    fields = ('device', 'zone', 'image',)


class VenueInline(admin.TabularInline):
    model = Ad.venues.through


class AdAdminForm(forms.ModelForm):
    class Meta:
        exclude = ('venues',)


class AdAdmin(admin.ModelAdmin):
    form = AdAdminForm
    list_display = [
        'title', 'url', 'advertiser', 'weight',
        'publication_date', 'publication_date_end']
    list_filter = [
        'publication_date', 'publication_date_end',
        'created_at', 'modified_at']
    search_fields = ['title', 'url']
    raw_id_fields = ['advertiser', 'created_by']
    inlines = (AdImageInline, VenueInline, )

    def get_changeform_initial_data(self, request):
        """
        Provide initial datas when creating an Ad.
        """
        get_data = super(AdAdmin, self).get_changeform_initial_data(request)
        return get_data or {
            'created_by': request.user.pk
        }


class ClickAdmin(admin.ModelAdmin):
    search_fields = ['ad__title', 'source_ip', 'session_id']
    list_display = ['ad', 'click_date', 'source_ip', 'session_id']
    list_filter = ['ad', 'click_date']
    date_hierarchy = 'click_date'
    actions = ['download_clicks']

    def get_queryset(self, request):
        qs = super(ClickAdmin, self).get_queryset(request)
        return qs.select_related('ad', 'ad__advertiser')

    def download_clicks(self, request, queryset):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="clicks.csv"'
        writer = csv.writer(response)
        writer.writerow(('Title',
                         'Advertised URL',
                         'Source IP',
                         'Timestamp',
                         'Advertiser ID',
                         'Advertiser name'))
        for click in queryset:
            writer.writerow((unicode(click.ad.title).encode("utf-8"),
                             click.ad.url,
                             click.source_ip,
                             click.click_date.isoformat(),
                             click.ad.advertiser.pk,
                             unicode(click.ad.advertiser.company_name).encode(
                                 "utf-8"),
                             unicode(click.ad.zone).encode("utf-8")))
        return response
    download_clicks.short_description = "Download selected Ad Clicks"


class ImpressionAdmin(admin.ModelAdmin):
    search_fields = ['ad__title', 'source_ip', 'session_id', 'venue']
    list_display = ['ad', 'impression_date',
                    'source_ip', 'session_id', 'venue', 'url']
    list_filter = ['ad', 'impression_date']
    date_hierarchy = 'impression_date'
    actions = ['download_impressions']

    def get_queryset(self, request):
        qs = super(ImpressionAdmin, self).get_queryset(request)
        return qs.select_related('ad', 'ad__advertiser')

    def download_impressions(self, request, queryset):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="impressions.csv"'
        writer = csv.writer(response)
        writer.writerow(('Title',
                         'Advertised URL',
                         'Source IP',
                         'Timestamp',
                         'Advertiser ID',
                         'Advertiser name'))
        for impression in queryset:
            writer.writerow((unicode(impression.ad.title).encode("utf-8"),
                             impression.ad.url,
                             impression.source_ip,
                             impression.impression_date.isoformat(),
                             impression.ad.advertiser.pk,
                             unicode(impression.ad.advertiser.company_name).encode(
                                 "utf-8"),
                             unicode(impression.ad.zone).encode("utf-8")))
        return response
    download_impressions.short_description = "Download selected Ad Impressions"


admin.site.register(Advertiser, AdvertiserAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Venue, VenueAdmin)
admin.site.register(Ad, AdAdmin)
admin.site.register(Click, ClickAdmin)
admin.site.register(Impression, ImpressionAdmin)
