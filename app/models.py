from calendar import Calendar
from unicodedata import decimal
from wsgiref.handlers import format_date_time
from django.db import models
from django.contrib.auth.models import User

class Agency(models.Model):
    agency_id = models.CharField(primary_key=True, max_length=140)
    agency_name = models.CharField(max_length=140, default='')
    agency_url = models.CharField(max_length=140, default='')
    agency_timezone = models.CharField(max_length=140, default='Europe/Paris')
    agency_lang = models.CharField(max_length=140, default='fr')

class Calendar(models.Model):
    service_id = models.CharField(primary_key=True, max_length=140)
    monday = models.CharField(max_length=1, default='0')
    tuesday = models.CharField(max_length=1, default='0')
    wednesday = models.CharField(max_length=1, default='0')
    thursday = models.CharField(max_length=1, default='0')
    friday = models.CharField(max_length=1, default='0')
    saturday = models.CharField(max_length=1, default='0')
    sunday = models.CharField(max_length=1, default='0')
    start_date = models.CharField(max_length=8, default='YYYYDDMM')
    end_date = models.CharField(max_length=8, default='YYYYDDMM')

class Calendar_dates(models.Model):
    service_id = models.ForeignKey('Calendar', on_delete=models.CASCADE)
    date = models.CharField(max_length=8, default='YYYYDDMM')
    exception_type = models.CharField(max_length=1, default='1') 

    