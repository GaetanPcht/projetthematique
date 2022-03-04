"""projetthematique URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import include, path
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from app.views import HomeAPIView, AgencyAPIView, CalendarAPIView, CalendarDatesAPIView, GTFSToJsonAPIView, RoutesAPIView, ShapesAPIView, StopTimesAPIView, StopsAPIView, StopsExtensionsAPIView, TransfersAPIView, TripsAPIView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('', HomeAPIView),
    path('gtfs-to-json/agency/', AgencyAPIView.as_view()),
    path('gtfs-to-json/calendar/', CalendarAPIView.as_view()),
    path('gtfs-to-json/calendar-dates/', CalendarDatesAPIView.as_view()),
    path('gtfs-to-json/routes/', RoutesAPIView.as_view()),
    path('gtfs-to-json/shapes/', ShapesAPIView.as_view()),
    path('gtfs-to-json/stops/', StopsAPIView.as_view()),
    path('gtfs-to-json/stops-extensions/', StopsExtensionsAPIView.as_view()),
    path('gtfs-to-json/transfers/', TransfersAPIView.as_view()),
    path('gtfs-to-json/trips/', TripsAPIView.as_view()),
    path('gtfs-to-json/stop-times/', StopTimesAPIView.as_view()),
    path('gtfs-to-json/<test>', GTFSToJsonAPIView.as_view()),
]