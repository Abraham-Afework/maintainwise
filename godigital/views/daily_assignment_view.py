#views/digital_resume_views.py

from django.shortcuts import render
from django.template.loader import render_to_string
from django.http import HttpResponse
from ..models import Aircrafts,Faults,Technicians,Scheduledate
from ..forms import FaultForm
from datetime import datetime,timedelta

def daily_assignment(request):
    current_date = datetime.now().date()
    selected_date_str = request.GET.get('date')

    if selected_date_str:
        try:
            selected_date = datetime.strptime(selected_date_str, '%Y-%m-%d').date()
        except ValueError:
            selected_date = current_date
    else:
        selected_date = current_date

    schedules = Scheduledate.objects.filter(
        technician__fleet='B777-PAX',
        date=selected_date
    ).order_by('technician__emp_id')

    context = {
        'schedules': schedules,
        'selected_date': selected_date,
    }
    return render(request, 'daily_assignment/create_daily_assignment.html', context)
