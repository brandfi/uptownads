# Generated by Django 2.1.2 on 2019-01-24 05:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ads', '0021_remove_click_venue'),
    ]

    operations = [
        migrations.AddField(
            model_name='click',
            name='url',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='Url'),
        ),
        migrations.AddField(
            model_name='click',
            name='venue',
            field=models.CharField(blank=True, max_length=40, null=True, verbose_name='Venue'),
        ),
    ]