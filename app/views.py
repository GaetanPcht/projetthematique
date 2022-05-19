from calendar import calendar
from django.http import JsonResponse
import urllib.request, zipfile, os, glob, time, requests, json
from django.template.response import TemplateResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from datetime import date, datetime, time, timedelta
from app.models import (
    Agency,
    Calendar,
    Calendar_dates,
    Routes,
    Shapes,
    Stops,
    Stop_extensions,
    Transfers,
    Trips,
    Stop_times,
    ZipUrl,
)
from app.serializers import (
    AgencySerializer,
    CalendarDatesSerializer,
    CalendarSerializer,
    GTFSToJsonSerializer,
    RoutesSerializer,
    ShapesSerializer,
    StopTimesSerializer,
    StopsExtensionsSerializer,
    StopsSerializer,
    TransfersSerializer,
    TripsSerializer,
)


def HomeAPIView(request):
    #  # downloadGTFSFile()
    return TemplateResponse(request, "index.html")


class GTFSToJsonAPIView(APIView):    
    def get(self, *args, **kwargs):
        # telechargement des fichiers gtfs et mise à jour de la bdd si neccessaire
        #  # downloadGTFSFile()
        # récupération du nom de l'arret + mise en forme pour coller au format de la bdd
        stopParam = kwargs['stop']
        stopParam = stopParam.upper()
        entryDay = datetime.now()
        entryTime = entryDay.time()
        # Si un horraire est donné, on initialise les données d'heure de début et de fin
        if 'time' in kwargs:
            # date format "yyyymmdd-h:m:s"
            entryDay = datetime.strptime(kwargs['time'], '%Y%m%d-%H:%M:%S')
            entryTime = entryDay.time()
        # latestTime = (datetime.combine(date.today(), time(entryTime.hour, entryTime.minute, entryTime.second)) + timedelta(hours=1, minutes=30)).time()
        latestTime = (datetime.combine(date.today(), time(entryTime.hour, entryTime.minute, entryTime.second)) + timedelta(hours=1)).time()


        nextTransitTimes = []

        # On recherche dans la bdd une liste d'arrêts 
        try:
            stops = Stops.objects.filter(stop_name = stopParam )
        except Stops.DoesNotExist:
            stops = None
        if stops != None:
            stopSerializer = StopsSerializer(stops, many=True)
            # On ajoute chaque arrêt à la liste d'arrêts 
            for stop in stopSerializer.data:
                stopTimes = Stop_times.objects.filter(stop_id = stop["stop_id"])
                stopTimesSerializer = StopTimesSerializer(stopTimes, many=True)                
                for stopTime in stopTimesSerializer.data:
                    getTime = False
                    fullTime = ''
                    arrivalTime = stopTime["arrival_time"]
                    if arrivalTime[:2] == "24":
                        arrivalTime = "00" + arrivalTime[2:]
                    # Récupération des données comprises seulement entre les limites d'heures
                    # if 'time' in kwargs:
                    # Pour les heures au format : "24:06"
                    fullTime = str(entryDay.strftime('%Y%m%d')) + '-' + str(datetime.strptime(arrivalTime, '%H:%M:%S').time())
                    fullTime = datetime.strptime(fullTime, '%Y%m%d-%H:%M:%S').isoformat()
                    arrivalTime = datetime.strptime(arrivalTime, '%H:%M:%S').time()
                    if time_in_range(entryTime, latestTime, arrivalTime):
                        getTime = True
                    # else:
                    #     fullTime = str(date.today().strftime('%Y%m%d')) + '-' + str(datetime.strptime(arrivalTime, '%H:%M:%S').time())
                    #     fullTime = datetime.strptime(fullTime, '%Y%m%d-%H:%M:%S').isoformat()
                    #     getTime= True
                    if getTime:
                        trip = Trips.objects.get(trip_id = stopTime["trip_id"])
                        trip = TripsSerializer(trip, many=False)
                        trip = trip.data
                        getDay = False
                        # Une ligne peut changer d'horaires en fonction d'une période donnée, récupération des données comprises
                        # seulement sur la période recherchée
                        # if 'time' in kwargs:
                        day = None
                        try:
                            day = Calendar.objects.get(service_id = trip["service_id"])
                        except Calendar.DoesNotExist:
                            day = None
                            getDay = True
                        if day != None: 
                            day = CalendarSerializer(day, many=False)
                            day = day.data
                            dateStart = datetime.strptime(day["start_date"], '%Y%m%d')
                            dateEnd = datetime.strptime(day["end_date"], '%Y%m%d')
                            if day[entryDay.strftime("%A").lower()] == "1" and dateStart <= entryDay <= dateEnd:
                                getDay = True
                        # else:
                        #     getDay= True

                        if getDay:
                            route = Routes.objects.get(route_id = trip["route_id"])
                            route = RoutesSerializer(route, many=False)
                            route = route.data
                            background = ''
                            if route["route_color"] != '':
                                background = '#' + route["route_color"]
                            text = ''
                            if route["route_text_color"] != '':
                                text = '#' + route["route_text_color"]
                            # Ajout d'un nouvel arrêt à la liste d'arrêts
                            nextTransitTimes.append(
                                {
                                    "line" : route["route_short_name"],
                                    "stop" : stop["stop_name"],
                                    "direction" : route["route_long_name"],
                                    "time" : fullTime,
                                    "coordinates" : {
                                        "latitude" : stop["stop_lat"],
                                        "longitude" : stop["stop_lon"]
                                    },
                                    "colors" : {
                                        "background" : background,
                                        "text" : text
                                    },
                                }
                            )
        else:
            stopSerializer = {}
        # conversion au format json des données
        json_dump = json.dumps(nextTransitTimes)
        json_object = json.loads(json_dump)
        
        return Response(json_object)


class AgencyAPIView(APIView):
    def get(self, *args, **kwargs):
         # downloadGTFSFile()
        categories = Agency.objects.all()
        serializer = AgencySerializer(categories, many=True)
        return Response(serializer.data)



class CalendarAPIView(APIView):
    def get(self, *args, **kwargs):
         # downloadGTFSFile()
        categories = Calendar.objects.all()
        serializer = CalendarSerializer(categories, many=True)
        return Response(serializer.data)


class CalendarDatesAPIView(APIView):
    def get(self, *args, **kwargs):
         # downloadGTFSFile()
        categories = Calendar_dates.objects.all()
        serializer = CalendarDatesSerializer(categories, many=True)
        return Response(serializer.data)


class RoutesAPIView(APIView):
    def get(self, *args, **kwargs):
         # downloadGTFSFile()
        categories = Routes.objects.all()
        serializer = RoutesSerializer(categories, many=True)
        return Response(serializer.data)


class ShapesAPIView(APIView):
    def get(self, *args, **kwargs):
         # downloadGTFSFile()
        categories = Shapes.objects.all()
        serializer = ShapesSerializer(categories, many=True)
        return Response(serializer.data)


class StopsAPIView(APIView):
    def get(self, *args, **kwargs):
         # downloadGTFSFile()
        categories = Stops.objects.all()
        serializer = StopsSerializer(categories, many=True)
        return Response(serializer.data)


class StopsExtensionsAPIView(APIView):
    def get(self, *args, **kwargs):
         # downloadGTFSFile()
        categories = Stop_extensions.objects.all()
        serializer = StopsExtensionsSerializer(categories, many=True)
        return Response(serializer.data)


class TransfersAPIView(APIView):
    def get(self, *args, **kwargs):
         # downloadGTFSFile()
        categories = Transfers.objects.all()
        serializer = TransfersSerializer(categories, many=True)
        return Response(serializer.data)


class TripsAPIView(APIView):
    def get(self, *args, **kwargs):
         # downloadGTFSFile()
        categories = Trips.objects.all()
        serializer = TripsSerializer(categories, many=True)
        return Response(serializer.data)


class StopTimesAPIView(APIView):
    def get(self, *args, **kwargs):
         # downloadGTFSFile()
        categories = Stop_times.objects.all()
        serializer = StopTimesSerializer(categories, many=True)
        return Response(serializer.data)


def time_in_range(start, end, x):
    """Return true if x is in the range [start, end]"""
    if start <= end:
        return start <= x <= end
    else:
        return start <= x or x <= end