from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from ..models import Technicians,Schedule,Scheduledate
from django.contrib import messages
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect
from django.urls import reverse
import calendar
from datetime import datetime,timedelta
from django.db import IntegrityError
# from django.contrib import messages
from django.template.loader import render_to_string
from collections import defaultdict
# from django.db.models.functions import ExtractMonth, ExtractYear
# from itertools import groupby
# from calendar import monthrange, day_name
# from operator import attrgetter
from django.shortcuts import render
from django.http import JsonResponse
from django.db.models import Q




# @login_required
def index(request):


	return render(request, 'index.html')



def search_schedule(request):
    # Get the current month and year
    current_date = datetime.now()
    month = current_date.month
    year = current_date.year

    # Assuming `new_monthly_schedule` returns an HttpResponse object
    rendered_template = new_monthly_schedule(request)

    context = {
        'rendered_template': rendered_template.content.decode('utf-8'),  # Convert HttpResponse to string
        'month': month,
        'year': year
    }

    return render(request, 'search_schedule.html', context)



def single_tech(request,id):
	tech = Technicians.objects.get(id=id)
	context={
		'tech': tech
		}
	return render(request, 'single_tech.html', context)

def add_tech(request):

# 	if request.method == 'POST':
# 		form = PostForm(request.POST)
# 		if form.is_valid():
# 			form.save()
# 			return redirect('index')
# 	else:
# 		form = PostForm()
		return render(request, 'add_tech.html')

def login_view(request):
	if request.method == 'POST':
		form = AuthenticationForm(request, data=request.POST)
		if form.is_valid():
			username = form.cleaned_data.get('username')
			password = form.cleaned_data.get('password')
			messages.info(request, f"Captured Username: {username}")  # Display captured username
			user = authenticate(request, username=username, password=password)
			# print(f"Captured Username: {username}")
			if user is not None:
				login(request,user)
				return redirect('index')  # Replace 'home' with your desired redirect URL
			else:
				messages.error(request, "Invalid username or password.")
		else:
			messages.error(request, "Invalid username or password.")
	else:
		form = AuthenticationForm()
	return render(request, 'login.html', {'form': form})

def register(request):

	if request.method == 'POST':
		form = RegistrationForm(request.POST)
		if form.is_valid():
			form.save()
			return redirect('login')
	else:
		form = RegistrationForm()
	return render(request,'register.html',{'form':form})

def logout_view(request):
	logout(request)
	return redirect('login')

def all_tech(request):
	posts = Technicians.objects.all()

	context={
		'posts': posts
	}


	return render(request,'Technicians.html',context)


def get_month_data(year, month):
    month_data = []
    first_weekday, num_days = calendar.monthrange(year, month)
    weekday_names = calendar.day_name  # List of weekday names
    for day in range(1, num_days + 1):
        current_weekday = (first_weekday + day - 1) % 7
        month_data.append((day, weekday_names[current_weekday][:3]))  # Using weekday names
    return month_data


def day_off_month_year_data(request):

    current_year = datetime.now().year
    current_month = datetime.now().month + 1
    end_year = 2050
    years = range(current_year, end_year + 1)

    months = [
        {"value": 1, "name": "January"},
        {"value": 2, "name": "February"},
        {"value": 3, "name": "March"},
        {"value": 4, "name": "April"},
        {"value": 5, "name": "May"},
        {"value": 6, "name": "June"},
        {"value": 7, "name": "July"},
        {"value": 8, "name": "August"},
        {"value": 9, "name": "September"},
        {"value": 10, "name": "October"},
        {"value": 11, "name": "November"},
        {"value": 12, "name": "December"}
    ]

    day_off_choice = [
        ('Mon-Tue', 'Mon-Tue'),
        ('Tue-Wed', 'Tue-Wed'),
        ('Wed-Thur', 'Wed-Thur'),
        ('Thu-Fri', 'Thu-Fri'),
        ('Fri-Sat', 'Fri-Sat'),
        ('Sat-Sun', 'Sat-Sun'),
        ('Sun-Mon', 'Sun-Mon'),
    ]
    context = {
        'years': years,
        'months': months,
        'day_off_choice':day_off_choice,
        'current_month' :current_month
    }
    return context



def edit_schedule(request, emp_id, month, year):

    technician = get_object_or_404(Technicians, emp_id=emp_id)
    schedule = Scheduledate.objects.filter(technician=technician, date__year=year, date__month=month)
    # context_from_another_view = day_off_month_year_data(request)
    date = datetime(year, month, 1).date()

    # return HttpResponse(year)

    if request.method == 'POST':
        emp_id = request.POST.get('emp_id')
        shift = request.POST.get('shift')
        dayoff = request.POST.get('dayoff')
        month_year = request.POST.get('month_year')
        year, month = map(int, month_year.split('-'))
        technician = Technicians.objects.get(emp_id=emp_id)
        date = datetime(year, month, 1).date()


        # Redirect to a success page or another view

        # return redirect('search_schedule')

        return render(request, 'new_monthly_sch.html')

    context = {
            'schedule': schedule,
            'technician':technician,
            'month': month,
            'year':year

        }
    return render(request, 'edit_schedule.html', context)

def new_monthly_schedule(request):


    current_date = datetime.now()
    month = current_date.month
    year = current_date.year
    fleet ='B777-PAX'



    technician_schedules = defaultdict(list)
    if request.method == 'POST':
            # Get form data
        month_year = request.POST.get('month_year')
        fleet = request.POST.get('fleet')
        shift = request.POST.get('shift')


        # return HttpResponse(f"Month and Year: {month_year}, Fleet: {fleet}, Shift: {shift}")



        # Parse the month and year
        year, month = map(int, month_year.split('-'))

        schedules = Scheduledate.objects.filter(
                technician__fleet=fleet,
                date__month=month,
                date__year=year
                ).order_by('technician__emp_id')

        # Apply shift filter only if it is not "All"

        if shift == "M":
            schedules = schedules.filter(Q(shift='M') | Q(shift='O') |  Q(shift='LM') | Q(shift=f'{shift}-off') |  Q(shift='O-off'))

        elif shift == "LM":
            schedules = schedules.filter(Q(shift='LM') | Q(shift=f'{shift}-off'))

        elif shift == "O":
             schedules = schedules.filter(Q(shift='O') | Q(shift=f'{shift}-off'))

        elif shift == "E":
            schedules = schedules.filter(Q(shift='E') | Q(shift='LE')  | Q(shift=f'{shift}-off'))

        elif shift == "N":
            schedules = schedules.filter(Q(shift='N') | Q(shift=f'{shift}-off'))

        elif shift == "FT":
            schedules = schedules.filter(Q(shift='FT') | Q(shift=f'{shift}-off'))

        elif shift == "V":
            schedules = schedules.filter(Q(shift='V') | Q(shift=f'{shift}-off'))

        elif shift == "CH":
            schedules = schedules.filter(Q(shift='CH') | Q(shift=f'{shift}-off'))

        elif shift == "TR":
            schedules = schedules.filter(Q(shift='TR') | Q(shift=f'{shift}-off'))
    else:
         schedules = Scheduledate.objects.filter(
                technician__fleet=fleet,
                date__month=month,
                date__year=year
                ).order_by('technician__emp_id')





    technician_schedules = {}

    for schedule in schedules:
        technician_name = schedule.technician.name
        if technician_name not in technician_schedules:
            technician_schedules[technician_name] = {
                'technician': schedule.technician,
                'schedules': []
            }
        technician_schedules[technician_name]['schedules'].append({
            'shift': schedule.shift,
            'is_day_off': schedule.is_day_off,
            'date': schedule.date
        })

    days = get_month_data(year, month)

    context = {

        'days': days,
        'schedule_data': technician_schedules.values(),
        'year': year,
        'month': month,
        'fleet': fleet,
        'month_name': calendar.month_name[month]
    }
    return render(request, 'new_monthly_sch.html',context)

def monthly_schedule(request):

    if request.method == 'POST':
        # Get form data
        month_year = request.POST.get('month_year')
        fleet = request.POST.get('fleet')
        shift = request.POST.get('shift')



        # Parse the month and year
        year, month = map(int, month_year.split('-'))

    schedule = Schedule.objects.select_related('technician').filter(
        month=month,
        year=year,
        technician__fleet=fleet,

    )
    days = get_month_data(year, month)

    context = {
        'days': days,
        'schedule_data':schedule,
        'year': year,
        'month': month,
        'fleet': fleet,
		'month_name': calendar.month_name[month]

    }
    return render(request, 'monthly_sch.html',context)


def start_schedule(request):

    error_message = None
    technicians = Technicians.objects.all().order_by('emp_id')
    context_from_another_view = day_off_month_year_data(request)

    if request.method == 'POST':
        emp_id = request.POST.get('emp_id')
        shift = request.POST.get('shift')
        dayoff = request.POST.get('dayoff')
        month_year = request.POST.get('month_year')
        year, month = map(int, month_year.split('-'))
        technician = Technicians.objects.get(emp_id=emp_id)

        try:
            schedule = Schedule.objects.create(
                month=month,
                year=year,
                technician=technician,
                shift=shift,
                dayoff=dayoff
            )
        except IntegrityError:
                error_message = f'Schedule already exists for {technician.name}, month, and year'
                messages.error(request, error_message)

        if not error_message:
            return redirect('monthly_schedule')

    context = {
        **context_from_another_view,
        'technicians': technicians,
        'error_message': error_message
    }

    return render(request, 'start_schedule.html', context)


def get_employee_name(request):
    emp_id = request.GET.get('emp_id')
    try:
        technician = Technicians.objects.get(emp_id=emp_id)
        response_html = f'<input type="text" class="form-control" id="employee_id""  value="{technician.emp_id}" disabled> '
        return HttpResponse(response_html)
    except Technicians.DoesNotExist:
        response_html = '<input type="text" class="form-control" id="employee_id"  value="Employee not found" disabled>'
        return HttpResponse(response_html, status=404)

def export_schedule_to_excel(request):
    # Get the schedules from the database
    schedules = Schedule.objects.all()

    # Set the start year and month (these could be dynamic based on your application's requirements)
    start_year = datetime.now().year
    start_month = datetime.now().month

    # Generate the Excel workbook
    workbook = generate_excel(schedules, start_year, start_month)

    # Set the content type and the filename
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = f'attachment; filename=schedule_{start_month}_{start_year}.xlsx'

    # Save the workbook to the response
    workbook.save(response)
    return response


def custom_404_view(request, exception):
    html = render_to_string('404.html', {})
    return HttpResponseNotFound(html)

 # Adjust as per your models

def schedule_create_batch(request):
    if request.method == 'POST':
        # Example: Process batch creation of schedules
        schedule_forms = request.POST.getlist('schedule-form')

        for schedule_data in schedule_forms:
            emp_id = schedule_data.get('emp_id')
            name = schedule_data.get('name')
            start_date = schedule_data.get('start_date')
            end_date = schedule_data.get('end_date')
            shift = schedule_data.get('shift')
            day_off = schedule_data.get('day_off')

            # Process each schedule form data as needed (create or update Scheduledate objects)
            # Scheduledate.objects.create(
            #     emp_id=emp_id,
            #     name=name,
            #     start_date=start_date,
            #     end_date=end_date,
            #     shift=shift,
            #     day_off=day_off
            # )

        # Example response: Return JSON response or HTML content if needed
        # return JsonResponse({'message': 'Schedules created successfully.'})

    # Handle GET requests or render form initially (not shown for brevity)

        return render(request, 'test.html', {'schedules': schedule_forms})


def schedule_form_template(request):
    # Additional context data can be passed if necessary
    return render(request, 'schedule_form.html')


@login_required
def schedule_create(request):
    error_message = None
    technicians = Technicians.objects.all().order_by('emp_id')
    context_from_another_view = day_off_month_year_data(request)

    if request.method == 'POST':
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        shift = request.POST.get('shift')
        day_off = request.POST.get('day_off')
        emp_id = request.POST.get('emp_id')
        technician = Technicians.objects.get(emp_id=emp_id)



        # Parse day off input
        day_off_days = []
        if 'mon' in day_off.lower():
            day_off_days.append(0)  # Monday
        if 'tue' in day_off.lower():
            day_off_days.append(1)  # Tuesday
        if 'wed' in day_off.lower():
            day_off_days.append(2)  # Wednesday
        if 'thu' in day_off.lower():
            day_off_days.append(3)  # Thursday
        if 'fri' in day_off.lower():
            day_off_days.append(4)  # Friday
        if 'sat' in day_off.lower():
            day_off_days.append(5)  # Saturday
        if 'sun' in day_off.lower():
            day_off_days.append(6)  # Sunday

        # Convert string dates to datetime objects
        start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
        end_date = datetime.strptime(end_date, '%Y-%m-%d').date()

        # Loop through each date in the range and create or update Schedule instances
        current_date = start_date
        while current_date < end_date + timedelta(days=1):
            if current_date.weekday() in day_off_days:
                # Check if an entry exists
                schedule_entries = Scheduledate.objects.filter(
                    technician=technician,
                    date=current_date,
                )

                if schedule_entries.exists():
                    for schedule_entry in schedule_entries:
                        schedule_entry.is_day_off = True
                        schedule_entry.shift = f"{shift}-off"
                        schedule_entry.save()
                else:
                    # Create a new entry if no existing entry found
                    Scheduledate.objects.create(
                        technician=technician,
                        date=current_date,
                        is_day_off=True,
                        shift=f"{shift}-off"
                    )
            else:
                # Check if an entry exists
                schedule_entries = Scheduledate.objects.filter(
                    technician=technician,
                    date=current_date,
                )

                if schedule_entries.exists():
                    for schedule_entry in schedule_entries:
                        schedule_entry.shift = shift
                        schedule_entry.is_day_off = False
                        schedule_entry.save()
                else:
                    # Create a new entry if no existing entry found
                    Scheduledate.objects.create(
                        technician=technician,
                        date=current_date,
                        shift=shift,
                        is_day_off=False
                    )

            current_date += timedelta(days=1)

        # Redirect after successful submission
        # return redirect('monthly_schedule')  # Redirect to a view where you can display the list of schedules

    context = {
        **context_from_another_view,
        'technicians': technicians,
        'error_message': error_message
    }

    return render(request, 'schedule_create.html', context)


def schedule_create_or_edit(request, emp_id):

    error_message = None
    technicians = Technicians.objects.filter(emp_id=emp_id)
    context_from_another_view = day_off_month_year_data(request)

    if emp_id:
        technician = get_object_or_404(Technicians, emp_id=emp_id)

    if request.method == 'POST':
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        shift = request.POST.get('shift')
        day_off = request.POST.get('day_off')
        if not technician:
            emp_id = request.POST.get('emp_id')
            technician = Technicians.objects.get(emp_id=emp_id)

        # Parse day off input
        day_off_days = []
        if 'mon' in day_off.lower():
            day_off_days.append(0)  # Monday
        if 'tue' in day_off.lower():
            day_off_days.append(1)  # Tuesday
        if 'wed' in day_off.lower():
            day_off_days.append(2)  # Wednesday
        if 'thu' in day_off.lower():
            day_off_days.append(3)  # Thursday
        if 'fri' in day_off.lower():
            day_off_days.append(4)  # Friday
        if 'sat' in day_off.lower():
            day_off_days.append(5)  # Saturday
        if 'sun' in day_off.lower():
            day_off_days.append(6)  # Sunday

        # Convert string dates to datetime objects
        start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
        end_date = datetime.strptime(end_date, '%Y-%m-%d').date()

        # Loop through each date in the range and create or update Schedule instances
        current_date = start_date
        while current_date <= end_date:
            if current_date.weekday() in day_off_days:
                # Check if an entry exists
                schedule_entries = Scheduledate.objects.filter(
                    technician=technician,
                    date=current_date,
                )

                if schedule_entries.exists():
                    for schedule_entry in schedule_entries:
                        schedule_entry.is_day_off = True
                        schedule_entry.shift = f"{shift}-off"
                        schedule_entry.save()
                else:
                    # Create a new entry if no existing entry found
                    Scheduledate.objects.create(
                        technician=technician,
                        date=current_date,
                        is_day_off=True,
                        shift=f"{shift}-off"
                    )
            else:
                # Check if an entry exists
                schedule_entries = Scheduledate.objects.filter(
                    technician=technician,
                    date=current_date,
                )

                if schedule_entries.exists():
                    for schedule_entry in schedule_entries:
                        schedule_entry.shift = shift
                        schedule_entry.is_day_off = False
                        schedule_entry.save()
                else:
                    # Create a new entry if no existing entry found
                    Scheduledate.objects.create(
                        technician=technician,
                        date=current_date,
                        shift=shift,
                        is_day_off=False
                    )

            current_date += timedelta(days=1)

        # return redirect('schedule_list')  # Redirect to a view where you can display the list of schedules

    context = {
        **context_from_another_view,
        'technicians': technicians,
        'error_message': error_message,
        'technician': technician
    }

    return render(request, 'schedule_create_or_edit.html', context)

def delete_schedule(request, emp_id, month, year):
    technician = get_object_or_404(Technicians, emp_id=emp_id)
    schedules = Scheduledate.objects.filter(technician=technician, date__year=year, date__month=month)

    if request.method == 'POST':
        schedules.delete()

        # Get the previous URL from the session (if available)
        previous_url = request.session.get('previous_url')

        if previous_url:
            # Clear the stored previous URL from session
            del request.session['previous_url']
            return HttpResponseRedirect(previous_url)

        # Redirect to a default URL or view if no previous URL stored
        return redirect('search_schedule')  # Redirect to search_schedule if no previous URL stored

    # Store the current URL as the previous URL in session
    request.session['previous_url'] = request.META.get('HTTP_REFERER', reverse('search_schedule'))

    # Handle other HTTP methods if necessary

    # Return a response if not POST (optional)




def confirm_delete_schedule(request, emp_id, month, year):

    technician = get_object_or_404(Technicians, emp_id=emp_id)
    month_name = Scheduledate.objects.filter(date__month=month).first().date.strftime('%B')

    context = {
        'technician': technician,
        'month': month,
        'year': year,
        'month_name': month_name,
    }
    return render(request, 'confirm_delete_schedule.html', context)
























def crew_schedule_pdf(request):
    # Fetch data from the database
    fleet = "B777-PAX"
    month_name = datetime.now().strftime('%B')
    current_year = datetime.now().year
    current_month = datetime.now().month
    days = [(i, datetime(current_year, current_month, i).strftime('%A')) for i in range(1, 16)]

    technicians = Technicians.objects.all()
    schedule_data = []

    for technician in technicians:
        schedules = Schedule.objects.filter(technician=technician, date__month=current_month)
        schedule_data.append({
            "technician": technician,
            "schedules": schedules
        })

    context = {
        'fleet': fleet,
        'month_name': month_name,
        'days': days,
        'schedule_data': schedule_data,
    }

    # Render the template
    html_string = render_to_string('crew_schedule_pdf.html', context)
    html = HTML(string=html_string)
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename=crew_schedule.pdf'
    html.write_pdf(target=response)

def test1(request):
    Technicians.objects.all().delete()
    return HttpResponse("All records deleted successfully.")


def test(request):

        technicians_data = """
            11351 MARTIN WOLDEKOBRE CAT B1/B2
            21455 AMANUEL ASCHALEW CAT B1/B2
            17325 MULUGETA CHECKLIE CAT B1/B2
            21464 HENOK KEBEDE CAT B1/B2
            21451 HABTAMU MENGISTE CAT B1/B2
            21486 DEMEWOZ ALEBEL CAT B1/B2
            20478 TESFAHUN MEKONNEN CAT B1/B2
            27294 ANTALEM DESSIE CAT B1/B2
            29273 GUDETA OLUMA MECH II
            29263 KUMA TEFERI MECH II
            34819 SISAY ZENAMARKOS MECH I
            34823 YALEW TESHALE MECH I
            34827 GIRMA AYALEW MECH I
            15938 MESFIN MOLA CAT B1/B2
            20789 KLINTON TAMIRU CAT B1/B2
            20786 TEGENE BELAY CAT B1/B2
            19332 BEFEKADU LEGESE CAT B1/B2
            20811 ABERA KENENI CAT B1/B2
            21450 YEABTSEGA YISEHAK CAT B1/B2
            21456 GEBRU BESHA CAT B1/B2
            27297 NEBIAT KEBEDE CAT B1/B2
            27292 KIDUS YOHANES CAT B1/B2
            34829 MULUMEBET SEMAGN MECH I
            34831 FRAZER TAWEKE MECH I
            34837 GEDAMNEH AKLILU MECH I
            17088 HENOK GEBRE CAT B1/B2
            16042 SAMSOM MENGISTE CAT C
            20788 DAWIT WEDAJ CAT B1/B2
            20797 ABRAHAM AFEWORK CAT C
            21443 ASHENAFI YEMANE CAT B1/B2
            21444 ANDUALEM WORKU CAT B1/B2
            21487 MICHAEL LELISA CAT B1/B2
            21484 DAWIT ALEMAYEHU CAT B1/B2
            27291 NATNAEL GEREMEW CAT B1/B2
            27300 WENDAFERAHU DESTA MECH II
            29245 EFREM FISEHA MECH II
            """

        technicians_list = [
            {
                "emp_id": parts[0],
                "name": ' '.join(parts[1:-2]),
                "position": f"{parts[-2]} {parts[-1]}"

            }
            for line in technicians_data.strip().split("\n")
            for parts in [line.split()]
        ]

        for tech in technicians_list:
            Technicians.objects.create(
                name=tech["name"],
                emp_id=tech["emp_id"],
                position=tech["position"],
                fleet="B777-PAX"
            )
        return HttpResponse("All records deleted successfully.")