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
        downloadGTFSFile()
        categories = Agency.objects.all()
        serializer = GTFSToJsonSerializer(categories, many=True)
        # return Response(serializer.data)
        return JsonResponse({"GTFSToJsonAPIView": "test"})


class AgencyAPIView(APIView):
    def get(self, *args, **kwargs):
        downloadGTFSFile()
        categories = Agency.objects.all()
        serializer = AgencySerializer(categories, many=True)
        return Response(serializer.data)
        # return JsonResponse({"AgencyAPIView": "test"})



class CalendarAPIView(APIView):
    def get(self, *args, **kwargs):
        downloadGTFSFile()
        categories = Calendar.objects.all()
        serializer = CalendarSerializer(categories, many=True)
        return JsonResponse({"CalendarAPIView": "test"})


class CalendarDatesAPIView(APIView):
    def get(self, *args, **kwargs):
        downloadGTFSFile()
        categories = Calendar_dates.objects.all()
        serializer = CalendarDatesSerializer(categories, many=True)
        return JsonResponse({"CalendarDatesAPIView": "test"})


class RoutesAPIView(APIView):
    def get(self, *args, **kwargs):
        downloadGTFSFile()
        categories = Routes.objects.all()
        serializer = RoutesSerializer(categories, many=True)
        return JsonResponse({"RoutesAPIView": "test"})


class ShapesAPIView(APIView):
    def get(self, *args, **kwargs):
        downloadGTFSFile()
        categories = Shapes.objects.all()
        serializer = ShapesSerializer(categories, many=True)
        return JsonResponse({"ShapesAPIView": "test"})


class StopsAPIView(APIView):
    def get(self, *args, **kwargs):
        downloadGTFSFile()
        categories = Stops.objects.all()
        serializer = StopsSerializer(categories, many=True)
        return JsonResponse({"StopsAPIView": "test"})


class StopsExtensionsAPIView(APIView):
    def get(self, *args, **kwargs):
        downloadGTFSFile()
        categories = Stop_extensions.objects.all()
        serializer = StopsExtensionsSerializer(categories, many=True)
        return JsonResponse({"StopsExtensionsAPIView": "test"})


class TransfersAPIView(APIView):
    def get(self, *args, **kwargs):
        downloadGTFSFile()
        categories = Transfers.objects.all()
        serializer = TransfersSerializer(categories, many=True)
        return JsonResponse({"TransfersAPIView": "test"})


class TripsAPIView(APIView):
    def get(self, *args, **kwargs):
        downloadGTFSFile()
        categories = Trips.objects.all()
        serializer = TripsSerializer(categories, many=True)
        return JsonResponse({"TripsAPIView": "test"})


class StopTimesAPIView(APIView):
    def get(self, *args, **kwargs):
        downloadGTFSFile()
        categories = Stop_times.objects.all()
        serializer = StopTimesSerializer(categories, many=True)
        return JsonResponse({"StopTimesAPIView": "test"})


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
    return True

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
            agency =  Agency.objects.create(agency_id = data[0], agency_name=data[1], agency_url=data[2], agency_timezone=data[3], agency_lang=data[4])
            agency.save()
    calendar_datesFile = open("data_to_import/calendar_dates.txt", "r")
    # for i, line in enumerate(calendar_datesFile.read().split('\n')):
    #     if line != '' and i != 0:
    #         data = line.split(',')
    #         agency =  Agency.objects.create(agency_id = data[0], agency_name=data[1], agency_url=data[2], agency_timezone=data[3], agency_lang=data[4])
    #         agency.save()
    calendarFile = open("data_to_import/calendar.txt", "r")
    routesFile = open("data_to_import/routes.txt", "r")
    shapesFile = open("data_to_import/shapes.txt", "r")
    stop_extensionsFile = open("data_to_import/stop_extensions.txt", "r")
    stop_timesFile = open("data_to_import/stop_times.txt", "r")
    stopsFile = open("data_to_import/stops.txt", "r")
    transfersFile = open("data_to_import/transfers.txt", "r")
    tripsFile = open("data_to_import/trips.txt", "r")
    # print(agencyFile.read())