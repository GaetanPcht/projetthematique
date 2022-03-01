from rest_framework.serializers import ModelSerializer
 
from app.models import Agency, Calendar, Calendar_dates, Routes, Shapes, Stop_extensions, Stop_times, Stops, Transfers, Trips

class GTFSToJsonSerializer(ModelSerializer):
 
    class Meta:
        model = Agency, Calendar
        fields = ['agency_id', 'agency_name']

class AgencySerializer(ModelSerializer):
 
    class Meta:
        model = Agency
        fields = ['agency_id', 'agency_name']


class CalendarSerializer(ModelSerializer):
 
    class Meta:
        model = Calendar
        fields = ['agency_id', 'agency_name']

class CalendarDatesSerializer(ModelSerializer):
 
    class Meta:
        model = Calendar_dates
        fields = ['agency_id', 'agency_name']

class RoutesSerializer(ModelSerializer):
 
    class Meta:
        model = Routes
        fields = ['agency_id', 'agency_name']

class ShapesSerializer(ModelSerializer):
 
    class Meta:
        model = Shapes
        fields = ['agency_id', 'agency_name']

class StopsSerializer(ModelSerializer):
 
    class Meta:
        model = Stops
        fields = ['agency_id', 'agency_name']

class StopsExtensionsSerializer(ModelSerializer):
 
    class Meta:
        model = Stop_extensions
        fields = ['agency_id', 'agency_name']

class TransfersSerializer(ModelSerializer):
 
    class Meta:
        model = Transfers
        fields = ['agency_id', 'agency_name']

class TripsSerializer(ModelSerializer):
 
    class Meta:
        model = Trips
        fields = ['agency_id', 'agency_name']

class StopTimesSerializer(ModelSerializer):
 
    class Meta:
        model = Stop_times
        fields = ['agency_id', 'agency_name']