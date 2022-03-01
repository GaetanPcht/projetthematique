from rest_framework.serializers import ModelSerializer

from app.models import (
    Agency,
    Calendar,
    Calendar_dates,
    Routes,
    Shapes,
    Stop_extensions,
    Stop_times,
    Stops,
    Transfers,
    Trips,
)


class GTFSToJsonSerializer(ModelSerializer):
    class Meta:
        model = Agency, Calendar
        fields = ["agency_id", "agency_name"]


class AgencySerializer(ModelSerializer):
    class Meta:
        model = Agency
        fields = [
            "agency_id",
            "agency_name",
            "agency_url",
            "agency_timezone",
            "agency_lang",
        ]


class CalendarSerializer(ModelSerializer):
    class Meta:
        model = Calendar
        fields = [
            "service_id",
            "monday",
            "tuesday",
            "wednesday",
            "thursday",
            "friday",
            "saturday",
            "sunday",
            "start_date",
            "end_date",
        ]


class CalendarDatesSerializer(ModelSerializer):
    class Meta:
        model = Calendar_dates
        fields = ["service_id", "date", "exception_type"]


class RoutesSerializer(ModelSerializer):
    class Meta:
        model = Routes
        fields = [
            "route_id",
            "agency_id",
            "route_short_name",
            "route_long_name",
            "route_desc",
            "route_type",
            "route_url",
            "route_color",
            "route_text_color",
        ]


class ShapesSerializer(ModelSerializer):
    class Meta:
        model = Shapes
        fields = ["shape_id", "shape_pt_lon", "shape_pt_lat", "shape_pt_sequence"]


class StopsSerializer(ModelSerializer):
    class Meta:
        model = Stops
        fields = [
            "stop_id",
            "stop_name",
            "stop_desc",
            "stop_lat",
            "stop_lon",
            "zone_id",
            "stop_url",
            "location_type",
            "parent_station",
            "wheelchair_boarding",
        ]


class StopsExtensionsSerializer(ModelSerializer):
    class Meta:
        model = Stop_extensions
        fields = ["object_id", "object_system", "object_code"]


class TransfersSerializer(ModelSerializer):
    class Meta:
        model = Transfers
        fields = ["from_stop_id", "to_stop_id", "transfer_type", "min_transfer_time"]


class TripsSerializer(ModelSerializer):
    class Meta:
        model = Trips
        fields = [
            "route_id",
            "service_id",
            "trip_id",
            "trip_headsign",
            "trip_short_name",
            "direction_id",
            "block_id",
            "wheelchair_accessible",
            "bikes_allowed",
            "trip_desc",
            "shape_id",
        ]


class StopTimesSerializer(ModelSerializer):
    class Meta:
        model = Stop_times
        fields = [
            "trip_id",
            "arrival_time",
            "departure_time",
            "stop_id",
            "stop_sequence",
            "stop_time_desc",
            "pickup_type",
            "drop_off_type",
        ]
