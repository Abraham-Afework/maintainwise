from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from .models import Technicians,Schedule
from .forms import RegistrationForm,Add_ScheduleForm
from django.contrib import messages
from django.http import HttpResponse
import calendar
from datetime import datetime
from django.db import IntegrityError
# from django.contrib import messages
import openpyxl
from openpyxl.styles import Font, Alignment
from datetime import datetime
from .models import Schedule
from .utils import generate_excel  # Import the helper function
# Create your views here.

#login_required
def index(request):


# 	context={
# 		'posts':
# 	}
	return render(request, 'index.html')

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
        ('Wed-Thu', 'Wed-Thu'),
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



def edit_schedule(request, id):

    schedule = get_object_or_404(Schedule, id=id)
    context_from_another_view = day_off_month_year_data(request)


    # # return HttpResponse("Missing required POST data", status=400)
    # if request.method == 'POST':

    #      schedule_id = request.POST.get('month_year')
    #      return HttpResponse(schedule_id)
    # #     shift = request.POST.get('shift')
    # #     dayoff = request.POST.get('dayoff')
    # #     month_year = request.POST.get('month_year')
    # #     year, month = map(int, month_year.split('-'))
    # #     technician = Technicians.objects.get(emp_id=emp_id)

    # #     Schedule.objects.update_or_create(
    # #         month=month,
    # #         year=year,
    # #         technician=technician,
    # #         defaults={
    # #             'shift': shift,
    # #             'dayoff': dayoff
    # #         }
    # #     )



    if request.method == 'POST':
        emp_id = request.POST.get('emp_id')
        shift = request.POST.get('shift')
        dayoff = request.POST.get('dayoff')
        month_year = request.POST.get('month_year')
        year, month = map(int, month_year.split('-'))
        technician = Technicians.objects.get(emp_id=emp_id)

        Schedule.objects.update_or_create(
            month=month,
            year=year,
            technician=technician,
            defaults={
                'shift': shift,
                'dayoff': dayoff
            }
        )
        return redirect('monthly_schedule')


    context = {
        **context_from_another_view,
        'schedule': schedule
        }
    # Your view logic here
    return render(request, 'edit_schedule.html', context)

def monthly_schedule(request):
	# Example year and month, can be dynamic
	year = 2024
	month = 6
	schedule = Schedule.objects.select_related('technician').filter(month=month)
	days = get_month_data(year, month)
	context = {
        'days': days,
        'schedule_data':schedule,
        'year': year,
        'month': month,
		'month_name': calendar.month_name[month]

    }

	return render(request, 'monthly_sch.html',context)

def start_schedule(request):

    error_message = None
    technicians = Technicians.objects.all()
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
        response_html = f'<input type="text" class="form-control" id="employee_name" name="employee_name" value="{technician.name}" disabled> '
        return HttpResponse(response_html)
    except Technicians.DoesNotExist:
        response_html = '<input type="text" class="form-control" id="employee_name" name="employee_name" value="Employee not found" disabled>'
        return HttpResponse(response_html, status=404)


# views.py

# views.py
def export_schedule_to_excel(request):
    # Define the start date of the month
    start_date = datetime.now()  # Or any specific date you want to start with
    start_year = start_date.year
    start_month = start_date.month

    # Fetch schedule data for the current month and year
    schedules = Schedule.objects.filter(month=start_month, year=start_year).select_related('technician')

    # Generate the Excel workbook
    wb = generate_excel(schedules, start_year, start_month)

    # Create a response object and set the content type and attachment headers
    response = HttpResponse(
        content=openpyxl.writer.excel.save_virtual_workbook(wb),
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = 'attachment; filename=schedule.xlsx'
    return response


# def add_schedule(request):

    # error_message = None

    # if request.method == 'POST':
    #     emp_id = request.POST.get('emp_id')
    #     shift = request.POST.get('shift')
    #     dayoff = request.POST.get('dayoff')
    #     month_year = request.POST.get('month_year')
    #     year, month = map(int, month_year.split('-'))
    #     technician = Technicians.objects.get(emp_id=emp_id)

    #     try:
    #         schedule = Schedule.objects.create(
    #             month=month,
    #             year=year,
    #             technician=technician,
    #             shift=shift,
    #             dayoff=dayoff
    #         )
    #     except IntegrityError:
    #         error_message = f'Schedule already exists for {technician.name}, month, and year'
    #         # messages.error(request, error_message)

    # if not error_message:
    #     return redirect('monthly_schedule')
    # return redirect('start_schedule', {'error_message': error_message})
