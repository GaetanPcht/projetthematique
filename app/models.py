from calendar import Calendar
from unicodedata import decimal
from wsgiref.handlers import format_date_time
from django.db import models
from django.contrib.auth.models import User

class Agency(models.Model):
    agency_id = models.CharField(primary_key=True)
    agency_name = models.CharField
    agency_url = models.URLField
    agency_timezone = models.CharField #A vérifier
    agency_lang = models.CharField

class Calendar(models.Model):
    service_id = models.IntegerField(primary_key=True)
    monday = models.IntegerField # valeurs 0 ou 1, boolean ou integer ? 
    tuesday = models.IntegerField # valeurs 0 ou 1, boolean ou integer ? 
    wednesday = models.IntegerField # valeurs 0 ou 1, boolean ou integer ? 
    thursday = models.IntegerField # valeurs 0 ou 1, boolean ou integer ? 
    friday = models.IntegerField # valeurs 0 ou 1, boolean ou integer ? 
    saturday = models.IntegerField # valeurs 0 ou 1, boolean ou integer ? 
    sunday = models.IntegerField # valeurs 0 ou 1, boolean ou integer ? 
    start_date = models.DateField
    end_date = models.DateField

class Calendar_dates(models.Model):
    service_id = models.IntegerField(primary_key=True)
    date = models.DateField
    exception_type = models.BooleanField

class Routes(models.Model):
    route_ip = models.CharField(primary_key=True)
    agency_id = models.ForeignKey(Agency.agency_id) #A vérifier
    route_short_name = models.CharField
    route_long_name = models.CharField
    route_desc = models.CharField
    route_type = models.CharField
    route_url = models.URLField
    route_color = models.CharField
    route_text_color = models.CharField

class Shapes(models.Model):
    shape_id = models.CharField(primary_key=True)
    shape_pt_lon = models.DecimalField(max_digits=9, decimal_places=6)
    shape_pt_lat = models.DecimalField(max_digits=9, decimal_places=6)
    shape_pt_sequence = models.IntegerField

class Stop_extensions(models.Model):
    object_id = models.CharField(primary_key=True)
    object_system = models.CharField
    object_code = models.CharField

class Stops(models.Model):
    stop_id = models.CharField(primary_key=True)
    stop_name = models.CharField
    stop_desc = models.CharField
    stop_lat = models.DecimalField(max_digits=9, decimal_places=6)
    stop_lon = models.DecimalField(max_digits=9, decimal_places=6)
    zone_id = models.CharField # champ vide, inconnu
    stop_url = models.URLField # champ vide, inconnu
    location_type = models.IntegerField  # valeurs 0 ou 1, boolean ou integer ? 
    parent_station = models.CharField
    wheelchair_boarding = models.IntegerField # valeurs 0 ou vide


class Stop_times(models.Model):
    trip_id = models.CharField(primary_key=True)
    arrival_time = models.TimeField
    departure_time = models.TimeField
    stop_id = models.ForeignKey(Stops.stop_id) #A vérifier
    stop_sequence = models.IntegerField
    stop_time_desc = models.CharField
    pickup_type = models.IntegerField  # valeurs 0 ou 1, boolean ou integer ? 
    drop_off_type = models.IntegerField # valeurs 0 ou 1, boolean ou integer ? 

class Transfers(models.Model):
    from_stop_id = models.ForeignKey(Stops.stop_id)
    to_stop_id = models.ForeignKey(Stops.stop_id)
    transfer_type = models.IntegerField # toujours égal à 2
    min_transfer_time = models.IntegerField # minutes sous format integer (29, 129, 178, ...)

class Trips(models.Model):
    route_id = models.ForeignKey(Routes.route_id)
    service_id = models.ForeignKey(Calendar_dates.service_id)
    trip_id = models.CharField(primary_key=True)
    trip_headsign = models.CharField
    trip_short_name = models.CharField # toujours vide
    direction_id  = models.IntegerField # valeurs 0 ou 1, boolean ou integer ? 
    block_id = models.IntegerField # valeurs 0 ou 1, boolean ou integer ? 
    wheelchair_accessible = models.IntegerField # valeurs 0 ou 1, boolean ou integer ? 
    bikes_allowed = models.IntegerField # valeurs 0 ou 1, boolean ou integer ? 
    trip_desc = models.CharField # toujours vide
    shape_id = models.ForeignKey(Shapes.shape_ip)





    
