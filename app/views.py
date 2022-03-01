from django.http import JsonResponse
import urllib.request, zipfile, os, glob, time
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


def downloadGTFSFile():
    print(round(time.time() - start_time, 1), "ending function")
    files = glob.glob("data_to_import/*")
    for f in files:
        os.remove(f)
    url = "https://transport-data-gouv-fr-resource-history-prod.cellar-c2.services.clever-cloud.com/1e116130-3670-496d-b8dc-cb8c628dd8b6/1e116130-3670-496d-b8dc-cb8c628dd8b6.20220217.120214.919497.zip"
    urllib.request.urlretrieve(url, "data_to_import/data.zip")

    with zipfile.ZipFile("data_to_import/data.zip", "r") as zip_ref:
        zip_ref.extractall("data_to_import")

    zipFile = glob.glob("data_to_import/data.zip")
    for f in zipFile:
        os.remove(f)
