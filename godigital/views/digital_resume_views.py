#views/digital_resume_views.py

from django.shortcuts import render
from django.template.loader import render_to_string
from django.http import HttpResponse
from ..models import Aircrafts,Faults
from ..forms import FaultForm

def digital_resume(request):

    faults = Faults.objects.all()

    # if request.method == "GET":
    #     aircraft_id = request.GET.get('aircraft')

    #     faults = Faults.objects.filter(aircraft_id=aircraft_id)


    return render(request, 'digital_resume.html',{'faults': faults})



def get_aircraft_name(request):

    if request.method == "GET":

        fleet = request.GET.get('fleet')

        aircrafts = Aircrafts.objects.filter(fleet=fleet)

    context = {
      'aircrafts': aircrafts,
    }
    options_html = render_to_string('digital_resume/partials/aircraft_reg.html',context)

    return HttpResponse(options_html)


def add_digital_resume(request):
    fleet_choices = [
        ('B777', 'Boeing 777'),
        ('B787', 'Boeing 787'),
        ('B737', 'Boeing 737'),
        ('B767', 'Boeing 767'),
        ('A350', 'Airbus A350'),
        ('Q400', 'Bombardier Q400'),
    ]

    if request.method == 'POST':
        form = FaultForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponse("success")  # Redirect to a success page or another view
    else:
        form = FaultForm()
        # return HttpResponse("hellow")



    context = {
        'fleet_choices': fleet_choices,
        'form': form
    }
    return render(request, 'digital_resume/add_resume.html',context)


def get_faults(request):

    aircraft_id = request.GET.get('aircraft')
    faults = Faults.objects.filter(aircraft_id=aircraft_id)
    return render(request, 'digital_resume/faults.html', {'faults': faults})
