from django.contrib import admin
from app.models import *


class AgencyAdmin(admin.ModelAdmin):
    list_display = (
        "agency_id",
        "agency_name",
        "agency_url",
        "agency_timezone",
        "agency_lang",
    )


admin.site.register(Agency, AgencyAdmin)


class CalendarAdmin(admin.ModelAdmin):
    list_display = (
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
    )


admin.site.register(Calendar, CalendarAdmin)


class Calendar_datesAdmin(admin.ModelAdmin):
    list_display = (
        "service_id",
        "date",
        "exception_type",
    )


admin.site.register(Calendar_dates, Calendar_datesAdmin)


class RoutesAdmin(admin.ModelAdmin):
    list_display = (
        "route_id",
        "agency_id",
        "route_short_name",
        "route_long_name",
        "route_desc",
        "route_type",
        "route_url",
        "route_color",
        "route_text_color",
    )


admin.site.register(Routes, RoutesAdmin)


class ShapesAdmin(admin.ModelAdmin):
    list_display = (
        "shape_id",
        "shape_pt_lon",
        "shape_pt_lat",
        "shape_pt_sequence",
    )


admin.site.register(Shapes, ShapesAdmin)


class StopsAdmin(admin.ModelAdmin):
    list_display = (
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
    )


admin.site.register(Stops, StopsAdmin)


class Stop_extensionsAdmin(admin.ModelAdmin):
    list_display = (
        "object_id",
        "object_system",
        "object_code",
    )


admin.site.register(Stop_extensions, Stop_extensionsAdmin)


class Stop_timesAdmin(admin.ModelAdmin):
    list_display = (
        "trip_id",
        "arrival_time",
        "departure_time",
        "stop_id",
        "stop_sequence",
        "stop_time_desc",
        "pickup_type",
        "drop_off_type",
    )


admin.site.register(Stop_times, Stop_timesAdmin)


class TransfersAdmin(admin.ModelAdmin):
    list_display = (
        "from_stop_id",
        "to_stop_id",
        "transfer_type",
        "min_transfer_time",
    )


admin.site.register(Transfers, TransfersAdmin)


class TripsAdmin(admin.ModelAdmin):
    list_display = (
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
    )


admin.site.register(Trips, TripsAdmin)
