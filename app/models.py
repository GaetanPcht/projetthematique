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
    #magouille, service_id n'est pas unique mais date si
    service_id = models.CharField(max_length=3, default='')
    date = models.CharField(primary_key=True, max_length=8, default='YYYYDDMM')
    exception_type = models.CharField(max_length=1, default='1') 

class Routes(models.Model):
    route_id = models.CharField(primary_key=True, max_length=140)
    agency_id = models.ForeignKey('Agency', on_delete=models.CASCADE) #LIEN VERS AGENCY
    route_short_name = models.CharField(max_length=140, default='')
    route_long_name = models.CharField(max_length=140, default='')
    route_desc = models.CharField(max_length=140, default='')
    route_type = models.CharField(max_length=140, default='')
    route_url = models.CharField(max_length=140, default='')
    route_color = models.CharField(max_length=6, default='')
    route_text_color = models.CharField(max_length=6, default='')

class Shapes(models.Model):
    shape_id = models.CharField(primary_key=True, max_length=140)
    shape_pt_lon = models.CharField(max_length=140, default='')
    shape_pt_lat = models.CharField(max_length=140, default='')
    shape_pt_sequence = models.CharField(max_length=1, default='0')

class Stops(models.Model):
    stop_id = models.CharField(primary_key=True,  max_length=140)
    stop_name = models.CharField(max_length=140, default='')
    stop_desc = models.CharField(max_length=140, default='')
    stop_lat = models.CharField(max_length=140, default='')
    stop_lon = models.CharField(max_length=140, default='')
    zone_id = models.CharField(max_length=140, default='')
    stop_url = models.CharField(max_length=140, default='')
    location_type = models.CharField(max_length=1, default='')
    parent_station = models.CharField(max_length=140, default='')
    wheelchair_boarding = models.CharField(max_length=1, default='')

class Stop_extensions(models.Model):
    object_id = models.CharField(primary_key=True, max_length=140)
    object_system = models.CharField(max_length=140, default='')
    object_code = models.CharField(max_length=140, default='')

class Transfers(models.Model):
    # Magouille, foreign key avec un nom différent
    from_stop_id = models.ForeignKey('Stops', related_name='stop_id_from', on_delete=models.CASCADE, default='') #LIEN VERS STOPS
    # Magouille, foreign key avec un nom différent
    to_stop_id = models.ForeignKey('Stops', related_name='stop_id_to', on_delete=models.CASCADE, default='') #LIEN VERS STOPS 
    transfer_type = models.CharField(max_length=1, default='2')
    min_transfer_time = models.CharField(max_length=3, default='')

class Trips(models.Model):
    route_id = models.ForeignKey('Routes', on_delete=models.CASCADE) #LIEN VERS ROUTES
    service_id = models.ForeignKey('Calendar', on_delete=models.CASCADE) #LIEN VERS CALENDAR
    trip_id = models.CharField(primary_key=True,  max_length=140)    
    trip_headsign = models.CharField(max_length=140, default='')
    trip_short_name = models.CharField(max_length=140, default='')
    direction_id  = models.CharField(max_length=140, default='') #ID qui ne pointe nulpart ?
    block_id = models.CharField(max_length=140, default='') #ID qui ne pointe nulpart ?
    wheelchair_accessible = models.CharField(max_length=1, default='')
    bikes_allowed =models.CharField(max_length=1, default='')
    trip_desc = models.CharField(max_length=140, default='')
    shape_id = models.ForeignKey('Shapes', on_delete=models.CASCADE) #LIEN VERS SHAPES
    
class Stop_times(models.Model):
    trip_id = models.ForeignKey('Trips', on_delete=models.CASCADE, default='DEFAULT') #LIEN VERS TRIPS
    arrival_time = models.TimeField(default='00:00:00')
    departure_time = models.TimeField(default='00:00:00')
    stop_id = models.ForeignKey('Stops', on_delete=models.CASCADE, default='DEFAULT') #LIEN VERS AGENCY
    stop_sequence = models.CharField(max_length=140, default='')
    stop_time_desc = models.CharField(max_length=1, default='')
    pickup_type = models.CharField(max_length=1, default='')
    drop_off_type = models.CharField(max_length=1, default='')
