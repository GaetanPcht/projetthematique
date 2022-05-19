from django.core.management.base import BaseCommand, CommandError
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
import urllib.request, zipfile, os, glob, requests, json
from django.conf import settings

class Command(BaseCommand):
    # def add_arguments(self, parser):
        # Positional arguments


    def handle(self, *args, **options):
        if self.checkUpdateFile():
            files = glob.glob("data_to_import/*")
            for f in files:
                os.remove(f)
            # telechargement des données ametis 
            url = ZipUrl.objects.get(zipurl_id = 0).get()
            urllib.request.urlretrieve(url, "data_to_import/data.zip")
            # dezip les données
            with zipfile.ZipFile("data_to_import/data.zip", 'r') as zip_ref:
                zip_ref.extractall("data_to_import")

            zipFile = glob.glob("data_to_import/data.zip")
            for f in zipFile:
                os.remove(f)
                # update de la bdd
            self.updateDB()
            self.stdout.write(self.style.SUCCESS('Database successfully updated'))


    def checkUpdateFile(self, *args, **options):

        url = settings.OPEN_DATA_URL
        headers = {"user-agent": "my-app/0.0.1"}
        response = requests.get(url, headers=headers)
        responseJSON = json.loads(response.text)
        try:
            # si l'url retenue en bdd est différente de l'url des données de transports, les documents gtfs ont été mis 
            # à jour, on renvoit True
            if ZipUrl.objects.get(zipurl_id = 0).get() != responseJSON["history"][0]["payload"]["permanent_url"]:
                zipurl =  ZipUrl.objects.create(zipurl_id = 0, zipurl_value=responseJSON["history"][0]["payload"]["permanent_url"])
                zipurl.save()
                return True
        except ZipUrl.DoesNotExist:
            zipurl =  ZipUrl.objects.create(zipurl_id = 0, zipurl_value=responseJSON["history"][0]["payload"]["permanent_url"])
            zipurl.save()
            return True
        return False # Mettre à True pour récupérer les données sans vérifier qu'elles existent

    # remplacement de l'ancienne bdd par la nouvelle
    def updateDB(self, *args, **options):
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
        agencyFile = open("data_to_import/agency.txt", encoding="UTF-8")
        for i, line in enumerate(agencyFile.read().split('\n')):
            if line != '' and i != 0:
                line = line.replace('"', '')
                data = line.split(',')
                agency =  Agency.objects.create(
                    agency_id = data[0], 
                    agency_name = data[1], 
                    agency_url = data[2], 
                    agency_timezone = data[3], 
                    agency_lang = data[4],
                )
                agency.save()
        calendar_datesFile = open("data_to_import/calendar_dates.txt", encoding="UTF-8")
        for i, line in enumerate(calendar_datesFile.read().split('\n')):
            if line != '' and i != 0:
                line = line.replace('"', '')
                data = line.split(',')
                calendar_dates =  Calendar_dates.objects.create(
                service_id = data[0], 
                date = data[1], 
                exception_type = data[2], 
                )
                calendar_dates.save()
        calendarFile = open("data_to_import/calendar.txt", encoding="UTF-8")
        for i, line in enumerate(calendarFile.read().split('\n')):
            if line != '' and i != 0:
                line = line.replace('"', '')
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
        routesFile = open("data_to_import/routes.txt", encoding="UTF-8")
        for i, line in enumerate(routesFile.read().split('\n')):
            if line != '' and i != 0:
                line = line.replace('"', '')
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
        shapesFile = open("data_to_import/shapes.txt", encoding="UTF-8")
        for i, line in enumerate(shapesFile.read().split('\n')):
            if line != '' and i != 0:
                line = line.replace('"', '')
                data = line.split(',')
                shapes =  Shapes.objects.create(
                shape_id = data[0], 
                shape_pt_lon = data[1], 
                shape_pt_lat = data[2], 
                shape_pt_sequence = data[3],
                )
                shapes.save()
        stop_extensionsFile = open("data_to_import/stop_extensions.txt", encoding="UTF-8")
        for i, line in enumerate(stop_extensionsFile.read().split('\n')):
            if line != '' and i != 0:
                line = line.replace('"', '')
                data = line.split(',')
                stop_extensions =  Stop_extensions.objects.create(
                object_id = data[0], 
                object_system = data[1], 
                object_code = data[2],
                )
                stop_extensions.save()
        stop_timesFile = open("data_to_import/stop_times.txt", encoding="UTF-8")
        for i, line in enumerate(stop_timesFile.read().split('\n')):
            if line != '' and i != 0:
                line = line.replace('"', '')
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
        stopsFile = open("data_to_import/stops.txt", encoding="UTF-8")
        for i, line in enumerate(stopsFile.read().split('\n')):
            if line != '' and i != 0:
                line = line.replace('"', '')
                data = line.split(',')
                stops =  Stops.objects.create(
                stop_id = data[0], 
                stop_name = data[1].upper(), 
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
        transfersFile = open("data_to_import/transfers.txt", encoding="UTF-8")
        for i, line in enumerate(transfersFile.read().split('\n')):
            if line != '' and i != 0:
                line = line.replace('"', '')
                data = line.split(',')
                transfers =  Transfers.objects.create(
                from_stop_id = data[0], 
                to_stop_id = data[1], 
                transfer_type = data[2], 
                min_transfer_time = data[3],
                )
                transfers.save()
        tripsFile = open("data_to_import/trips.txt", encoding="UTF-8")
        for i, line in enumerate(tripsFile.read().split('\n')):
            if line != '' and i != 0:
                line = line.replace('"', '')
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
    # def updateDB(self, *args, **options):
    #     for poll_id in options['poll_ids']:
    #         try:
    #             poll = Poll.objects.get(pk=poll_id)
    #         except Poll.DoesNotExist:
    #             raise CommandError('Poll "%s" does not exist' % poll_id)

    #         poll.opened = False
    #         poll.save()

    #         self.stdout.write(self.style.SUCCESS('Successfully closed poll "%s"' % poll_id))