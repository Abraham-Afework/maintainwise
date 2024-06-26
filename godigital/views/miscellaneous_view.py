#views/miscellaneous_view.py

from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.http import HttpResponse
from ..models import Technicians, FlightSchedule
from django.contrib import messages
from django.utils.dateparse import parse_date


def flight_schedule(request):

    flight_schedules = FlightSchedule.objects.all()
    context = {
        'flight_schedules': flight_schedules,
    }

    return render(request, 'miscellaneous/flight_schedule.html',context)
    # return render(request, 'miscellaneous/flight_schedule.html')


def add_flight_schedule(request):
    if request.method == 'POST':
        emp_id = request.POST.get('emp_id')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')

        # Parse the dates
        start_date = parse_date(start_date)
        end_date = parse_date(end_date)

        storage = messages.get_messages(request)
        storage.used = True

        if not start_date or not end_date:
            messages.error(request, 'Invalid dates provided.')
        elif end_date <= start_date:
            messages.error(request, 'End date must be greater than start date.')
        else:
            # Fetch the technician based on emp_id
            single_technician = get_object_or_404(Technicians, emp_id=emp_id)

            # Check if the technician already has a schedule
            if FlightSchedule.objects.filter(tech_name=single_technician).exists():
                messages.error(request, f'Technician {single_technician.name} already has a schedule.')
            else:
                try:
                    # Create the FlightSchedule entry
                    flight_schedule = FlightSchedule.objects.create(
                        tech_name=single_technician,
                        start_date=start_date,
                        end_date=end_date
                    )
                    messages.success(request, f'Schedule created successfully for {single_technician.name}')

                except Exception as e:
                    error_message = f'An error occurred: {str(e)}'
                    messages.error(request, error_message)

    # Fetch all technicians and flight schedules to display in the form
    all_technicians = Technicians.objects.filter(position='CAT B1/B2')
    flight_schedules = FlightSchedule.objects.all().order_by('start_date')

    context = {
        'technicians': all_technicians,
        'flight_schedules': flight_schedules,
        'user': request.user,
    }

    return render(request, 'miscellaneous/add_flight_schedule.html', context)
