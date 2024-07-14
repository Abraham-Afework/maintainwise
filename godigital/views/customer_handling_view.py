from django.shortcuts import render, redirect
from ..models import ServiceLog,OperatorAirline,Aircrafts
from ..forms import ServiceLogForm
from datetime import datetime
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
import pandas as pd


def log_list(request):
    month_year_str = request.GET.get('month_year')
    operator_airline_id = request.GET.get('operator_airline')

    logs = ServiceLog.objects.all()

    # Filter logs based on month_year
    if month_year_str:
        try:
            month_year = datetime.strptime(month_year_str, '%Y-%m')
            logs = logs.filter(date__year=month_year.year, date__month=month_year.month)
        except ValueError:
            # Handle invalid date format if needed
            pass

    # Filter logs based on operator_airline_id
    if operator_airline_id:
        logs = logs.filter(operator_airline_id=operator_airline_id)

    return render(request, 'customer_handling/log_list.html', {'logs': logs})

def operator_airline(request):
    now = datetime.now()
    customer_airlines = OperatorAirline.objects.all().order_by('airline_name')

    context = {
        'current_year': now.year,
        'current_month': now.month,
        'customer_airlines':customer_airlines
    }


    return render(request, 'customer_handling/all_customer.html', context)

def log_create(request):
    if request.method == 'POST':
        form = ServiceLogForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('log_list')
    else:
        form = ServiceLogForm()
    return render(request, 'customer_handling/log_form.html', {'form': form})


def export_to_excel(request):
    logs = ServiceLog.objects.all().values('date', 'aircraft_type', 'reg_no', 'flt_no', 'remarks', 'svc_chk_action_taken', 'arr_time', 'dep_time')
    df = pd.DataFrame(list(logs))
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=logs.xlsx'
    df.to_excel(response, index=False)
    return response


def load_reg_numbers(request):
    operator_id = request.GET.get('operator_airline')
    if operator_id:
        operator_airline = get_object_or_404(OperatorAirline, pk=operator_id)
        aircrafts = Aircrafts.objects.filter(operator_airline=operator_airline).order_by('aircraft_reg')
        options = [{'value': aircraft.id, 'text': f"{aircraft.aircraft_reg} "} for aircraft in aircrafts]
    else:
        options = []

    return render(request, 'customer_handling/partials/options_template.html', {'options': options})