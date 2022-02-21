from django.contrib import admin
from app.models import *


class AgencyAdmin(admin.ModelAdmin):
    list_display = ('agency_id', 'agency_name','agency_url', 'agency_timezone', 'agency_lang', )
admin.site.register(Agency, AgencyAdmin)

class CalendarAdmin(admin.ModelAdmin):
    list_display = ('service_id', 'monday','tuesday', 'wednesday','thursday', 'friday', 'saturday', 'sunday', 'start_date', 'end_date', )
admin.site.register(Calendar, CalendarAdmin)
