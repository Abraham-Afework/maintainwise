from django.contrib import admin
from .models import Technicians,Scheduledate,Aircrafts,Faults,FlightSchedule

admin.site.register(Technicians)
admin.site.register(Scheduledate)
admin.site.register(Aircrafts)
admin.site.register(Faults)
admin.site.register(FlightSchedule)