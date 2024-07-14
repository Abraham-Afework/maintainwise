from django.contrib import admin
from .models import Technicians,Scheduledate,Aircrafts,Faults,FlightSchedule,Profile,ServiceLog,OperatorAirline

admin.site.register(Technicians)
admin.site.register(Profile)
admin.site.register(Scheduledate)
admin.site.register(Aircrafts)
admin.site.register(Faults)
admin.site.register(FlightSchedule)
admin.site.register(ServiceLog)
admin.site.register(OperatorAirline)