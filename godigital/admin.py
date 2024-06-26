from django.contrib import admin
from .models import Technicians,Scheduledate,Aircrafts,Faults,FlightSchedule,CustomUser
from django.contrib.auth.admin import UserAdmin


# class CustomUserAdmin(UserAdmin):
#     model = CustomUser
#     list_display = ['username', 'email', 'first_name', 'last_name', 'position']
#     fieldsets = UserAdmin.fieldsets + (
#         (None, {'fields': ('position',)}),
#     )
#     add_fieldsets = UserAdmin.add_fieldsets + (
#         (None, {
#             'fields': ('position',),
#         }),
#     )

# admin.site.register(CustomUser, CustomUserAdmin)


admin.site.register(Technicians)
admin.site.register(Scheduledate)
admin.site.register(Aircrafts)
admin.site.register(Faults)
admin.site.register(FlightSchedule)