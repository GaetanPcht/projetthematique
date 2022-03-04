from calendar import calendar
from django.http import JsonResponse
import urllib.request, zipfile, os, glob, time, requests, json
from django.template.response import TemplateResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
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
    downloadGTFSFile()
    return TemplateResponse(request, "index.html")


class GTFSToJsonAPIView(APIView):    
    def get(self, *args, **kwargs):
        stop = '"' + kwargs['test'] + '"'
        stop = stop.upper().encode("utf-8")
       
        try:
            stops = Stops.objects.filter(stop_name = stop )

        except Stops.DoesNotExist:
            stops = None

        if stops != None:
            stopSerializer = StopsSerializer(stops, many=True)
            for stop in stopSerializer.data:
                stopTimes = Stop_times.objects.filter(stop_id = stop["stop_id"])
                stopTimesSerializer = StopTimesSerializer(stopTimes, many=True)
                print(stopTimesSerializer.data)

        else:
            stopSerializer = {}


        # print(stopSerializer.data)
        # class Way:
        #     def __init__(self, line, stop, direction, time, coordinates, colors):
        #         self.line = line
        #         self.stop = stop
        #         self.direction = direction
        #         self.time = time
        #         self.coordinates = coordinates
        #         self.colors = colors
        downloadGTFSFile()
        # way =  Way(1,2,3,4,5,6)
        # print(way)
        # categories['agency'] = Agency.objects.all()
        # categories['calendar'] = Calendar.objects.all()
        # categories['calendar_dates'] = Calendar_dates.objects.all()
        # categories['routes'] = Routes.objects.all()
        # categories['shapes'] = Shapes.objects.all()
        # categories['stops'] = Stops.objects.all()
        # categories['stop_times'] = Stop_times.objects.all()
        # categories['transfers'] = Transfers.objects.all()
        # categories['trips'] = Trips.objects.all()
        # categories['stop_extensions'] = Stop_extensions.objects.all()
        # serializer = GTFSToJsonSerializer(categories, many=True)
        # return Response(way)
        return Response(stopSerializer.data)


class AgencyAPIView(APIView):
    def get(self, *args, **kwargs):
        downloadGTFSFile()
        categories = Agency.objects.all()
        serializer = AgencySerializer(categories, many=True)
        return Response(serializer.data)



class CalendarAPIView(APIView):
    def get(self, *args, **kwargs):
        downloadGTFSFile()
        categories = Calendar.objects.all()
        serializer = CalendarSerializer(categories, many=True)
        return Response(serializer.data)


class CalendarDatesAPIView(APIView):
    def get(self, *args, **kwargs):
        downloadGTFSFile()
        categories = Calendar_dates.objects.all()
        serializer = CalendarDatesSerializer(categories, many=True)
        return Response(serializer.data)


class RoutesAPIView(APIView):
    def get(self, *args, **kwargs):
        downloadGTFSFile()
        categories = Routes.objects.all()
        serializer = RoutesSerializer(categories, many=True)
        return Response(serializer.data)


class ShapesAPIView(APIView):
    def get(self, *args, **kwargs):
        downloadGTFSFile()
        categories = Shapes.objects.all()
        serializer = ShapesSerializer(categories, many=True)
        return Response(serializer.data)


class StopsAPIView(APIView):
    def get(self, *args, **kwargs):
        downloadGTFSFile()
        categories = Stops.objects.all()
        serializer = StopsSerializer(categories, many=True)
        return Response(serializer.data)


class StopsExtensionsAPIView(APIView):
    def get(self, *args, **kwargs):
        downloadGTFSFile()
        categories = Stop_extensions.objects.all()
        serializer = StopsExtensionsSerializer(categories, many=True)
        return Response(serializer.data)


class TransfersAPIView(APIView):
    def get(self, *args, **kwargs):
        downloadGTFSFile()
        categories = Transfers.objects.all()
        serializer = TransfersSerializer(categories, many=True)
        return Response(serializer.data)


class TripsAPIView(APIView):
    def get(self, *args, **kwargs):
        downloadGTFSFile()
        categories = Trips.objects.all()
        serializer = TripsSerializer(categories, many=True)
        return Response(serializer.data)


class StopTimesAPIView(APIView):
    def get(self, *args, **kwargs):
        downloadGTFSFile()
        categories = Stop_times.objects.all()
        serializer = StopTimesSerializer(categories, many=True)
        return Response(serializer.data)


start_time = time.time()


# def downloadGTFSFile():
#     print(round(time.time() - start_time, 1), "ending function")
#     files = glob.glob("data_to_import/*")
#     for f in files:
#         os.remove(f)
#     url = "https://transport-data-gouv-fr-resource-history-prod.cellar-c2.services.clever-cloud.com/1e116130-3670-496d-b8dc-cb8c628dd8b6/1e116130-3670-496d-b8dc-cb8c628dd8b6.20220217.120214.919497.zip"
#     urllib.request.urlretrieve(url, "data_to_import/data.zip")

#     with zipfile.ZipFile("data_to_import/data.zip", "r") as zip_ref:
#         zip_ref.extractall("data_to_import")

#     zipFile = glob.glob("data_to_import/data.zip")
#     for f in zipFile:
#         os.remove(f)

def downloadGTFSFile():
    if checkUpdateFile():
        files = glob.glob("data_to_import/*")
        for f in files:
            os.remove(f)
        url = ZipUrl.objects.get(zipurl_id = 0).get()
        print(url)
        urllib.request.urlretrieve(url, "data_to_import/data.zip")

        with zipfile.ZipFile("data_to_import/data.zip", "r") as zip_ref:
            zip_ref.extractall("data_to_import")

        zipFile = glob.glob("data_to_import/data.zip")
        for f in zipFile:
            os.remove(f)
        updateDB()


def checkUpdateFile():
    url = "https://transport.data.gouv.fr/api/datasets/6033a87b4e276fd6499986bf"
    headers = {"user-agent": "my-app/0.0.1"}
    response = requests.get(url, headers=headers)
    responseJSON = json.loads(response.text)
    try:
        if ZipUrl.objects.get(zipurl_id = 0).get() != responseJSON["history"][0]["payload"]["permanent_url"]:
            zipurl =  ZipUrl.objects.create(zipurl_id = 0, zipurl_value=responseJSON["history"][0]["payload"]["permanent_url"])
            zipurl.save()
            return True
    except ZipUrl.DoesNotExist:
        zipurl =  ZipUrl.objects.create(zipurl_id = 0, zipurl_value=responseJSON["history"][0]["payload"]["permanent_url"])
        zipurl.save()
        return True
    return False # Mettre à True pour récupérer les données

def updateDB():
    Agency.objects.all().delete()
    Calendar_dates.objects.all().delete()
    Calendar.objects.all().delete()
    Routes.objects.all().delete()
    Shapes.objects.all().delete()
    Stop_extensions.objects.all().delete()
    Stop_times.objects.all().delete()
    Stops.objects.all().delete()
    Transfers.objects.all().delete()
    Trips.objects.all().delete()
    agencyFile = open("data_to_import/agency.txt", "r")
    for i, line in enumerate(agencyFile.read().split('\n')):
        if line != '' and i != 0:
            data = line.split(',')
            agency =  Agency.objects.create(
                agency_id = data[0], 
                agency_name = data[1], 
                agency_url = data[2], 
                agency_timezone = data[3], 
                agency_lang = data[4],
            )
            agency.save()
    calendar_datesFile = open("data_to_import/calendar_dates.txt", "r")
    for i, line in enumerate(calendar_datesFile.read().split('\n')):
        if line != '' and i != 0:
            data = line.split(',')
            calendar_dates =  Calendar_dates.objects.create(
              service_id = data[0], 
              date = data[1], 
              exception_type = data[2], 
            )
            calendar_dates.save()
    calendarFile = open("data_to_import/calendar.txt", "r")
    for i, line in enumerate(calendarFile.read().split('\n')):
        if line != '' and i != 0:
            data = line.split(',')
            calendar =  Calendar.objects.create(
              service_id = data[0], 
              monday = data[1],
              tuesday = data[2], 
              wednesday = data[3], 
              thursday = data[4],
              friday = data[5],
              saturday = data[6],
              sunday = data[7],
              start_date = data[8],
              end_date = data[9],
          )
            calendar.save()
    routesFile = open("data_to_import/routes.txt", "r")
    for i, line in enumerate(routesFile.read().split('\n')):
        if line != '' and i != 0:
            data = line.split(',')
            routes =  Routes.objects.create(
              route_id = data[0], 
              agency_id = data[1], 
              route_short_name = data[2], 
              route_long_name = data[3], 
              route_desc = data[4],
              route_type = data[5],
              route_url = data[6],
              route_color = data[7],
              route_text_color = data[8],
            )
            routes.save()
    shapesFile = open("data_to_import/shapes.txt", "r")
    for i, line in enumerate(shapesFile.read().split('\n')):
        if line != '' and i != 0:
            data = line.split(',')
            shapes =  Shapes.objects.create(
              shape_id = data[0], 
              shape_pt_lon = data[1], 
              shape_pt_lat = data[2], 
              shape_pt_sequence = data[3],
            )
            shapes.save()
    stop_extensionsFile = open("data_to_import/stop_extensions.txt", "r")
    for i, line in enumerate(stop_extensionsFile.read().split('\n')):
        if line != '' and i != 0:
            data = line.split(',')
            stop_extensions =  Stop_extensions.objects.create(
              object_id = data[0], 
              object_system = data[1], 
              object_code = data[2],
            )
            stop_extensions.save()
    stop_timesFile = open("data_to_import/stop_times.txt", "r")
    for i, line in enumerate(stop_timesFile.read().split('\n')):
        if line != '' and i != 0:
            data = line.split(',')
            stop_times =  Stop_times.objects.create(
              trip_id = data[0], 
              arrival_time = data[1], 
              departure_time = data[2], 
              stop_id = data[3], 
              stop_sequence = data[4],
              stop_time_desc = data[5],
              pickup_type = data[6],
              drop_off_type = data[7],
            )
            stop_times.save()
        # Supprimer pour tout insérer
        # if i == 100:
        #     break
    stopsFile = open("data_to_import/stops.txt", "r")
    for i, line in enumerate(stopsFile.read().split('\n')):
        if line != '' and i != 0:
            data = line.split(',')
            stops =  Stops.objects.create(
              stop_id = data[0], 
              stop_name = data[1].upper().encode('utf-8'), 
              stop_desc = data[2], 
              stop_lat = data[3], 
              stop_lon = data[4],
              zone_id = data[5],
              stop_url = data[6],
              location_type = data[7],
              parent_station = data[8],
              wheelchair_boarding = data[9],
            )
            stops.save()
    transfersFile = open("data_to_import/transfers.txt", "r")
    for i, line in enumerate(transfersFile.read().split('\n')):
        if line != '' and i != 0:
            data = line.split(',')
            transfers =  Transfers.objects.create(
              from_stop_id = data[0], 
              to_stop_id = data[1], 
              transfer_type = data[2], 
              min_transfer_time = data[3],
            )
            transfers.save()
    tripsFile = open("data_to_import/trips.txt", "r")
    for i, line in enumerate(tripsFile.read().split('\n')):
        if line != '' and i != 0:
            data = line.split(',')
            trips =  Trips.objects.create(
              route_id = data[0],
              service_id = data[1], 
              trip_id = data[2], 
              trip_headsign = data[3], 
              trip_short_name = data[4],
              direction_id = data[5],
              block_id = data[6],
              wheelchair_accessible = data[7],
              bikes_allowed = data[8],
              trip_desc = data[9],
              shape_id = data[10],
            )
            trips.save()