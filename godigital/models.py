from django.db import models
from datetime import datetime,timedelta
from django.contrib.auth.models import AbstractUser



class CustomUser(AbstractUser):
    position = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.username


class Technicians(models.Model):

	name = models.CharField(max_length=100)
	emp_id = models.CharField(max_length=10)
	position = models.CharField(max_length=100)
	fleet = models.CharField(max_length=10, null=True)


	def __str__(self):
		return self.name


class Schedule(models.Model):


    DAY_OFF_CHOICES = [
        ('Mon-Tue', 'Mon-Tue'),
        ('Tue-Wed', 'Tue-Wed'),
        ('Wed-Thu', 'Wed-Thu'),
        ('Thu-Fri', 'Thu-Fri'),
        ('Fri-Sat', 'Fri-Sat'),
        ('Sat-Sun', 'Sat-Sun'),
        ('Sun-Mon', 'Sun-Mon'),
    ]

    MONTH_CHOICES = [
        (1, 'Jan'),
        (2, 'Feb'),
        (3, 'Mar'),
        (4, 'Apr'),
        (5, 'May'),
        (6, 'Jun'),
        (7, 'Jul'),
        (8, 'Aug'),
        (9, 'Sep'),
        (10, 'Oct'),
        (11, 'Nov'),
        (12, 'Dec'),
    ]

    current_year = datetime.now().year
    YEAR_CHOICES = [(year, year) for year in range(current_year,current_year + 10)]


    technician = models.ForeignKey(Technicians, on_delete=models.CASCADE)
    shift = models.CharField(max_length=10)
    dayoff = models.CharField(max_length=8, choices=DAY_OFF_CHOICES)
    date = models.DateField(null=True)
    month = models.IntegerField(choices=MONTH_CHOICES)
    year = models.IntegerField(choices=YEAR_CHOICES)


    def __str__(self):
        return f"Schedule for {self.technician.name} - Shift: {self.shift}, Day Off: {self.dayoff}, Date: {self.date}"

    class Meta:
        # Ensure that month and year combination is unique for each technician
        unique_together = ('technician', 'month', 'year')

class MonthYear(models.Model):
    date = models.DateField()

    def __str__(self):
        return self.date.strftime('%B %Y')

class Scheduledate(models.Model):

    SHIFT_CHOICES = [
        ('M', 'Morning'),
         ('E', 'Evening'),
          ('N', 'Night'),
           ('FT', 'Flight'),
            ('TR', 'Training'),
            ('V', 'Vaccation'),


    ]

    technician = models.ForeignKey(Technicians, on_delete=models.CASCADE)
    date = models.DateField(default=datetime.now())
    shift = models.CharField(max_length=10, null=True, blank=True, choices=SHIFT_CHOICES)
    is_day_off = models.BooleanField(default=False)


    def __str__(self):
        return f"Schedule for {self.technician.name} - Shift: {self.shift}, Day Off: {self.is_day_off}, Date: {self.date}\n"

    class Meta:
        unique_together = ('technician', 'date', 'shift')


class Aircrafts(models.Model):

    FLEET_CHOICES = [
        ('B777', 'Boeing 777'),
        ('B787', 'Boeing 787'),
        ('B737', 'Boeing 737'),
        ('B767', 'Boeing 767'),
        ('A350', 'Airbus A350'),
        ('Q400', 'Bombardier Q400'),
    ]

    aircraft_reg = models.CharField(max_length=100)
    fleet = models.CharField(max_length=4, choices=FLEET_CHOICES)

    def __str__(self):
        return f"{self.aircraft_reg} - {self.get_fleet_display()}"


class Faults(models.Model):

    STATUS_CHOICES = [
        ('OPEN', 'Open'),
        ('IN_PROGRESS', 'In Progress'),
        ('RESOLVED', 'Resolved'),
        ('CLOSED', 'Closed'),
    ]

    aircraft = models.ForeignKey(Aircrafts, on_delete=models.CASCADE)
    faults = models.TextField()
    action_taken = models.TextField(blank=True,null=True)
    found_date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='OPEN',null=True)
    created_by = models.ForeignKey(Technicians, on_delete=models.PROTECT,null=True)

    def __str__(self):
        return f"{self.aircraft.aircraft_reg} - {self.status}"

###########################################################################################

class FlightSchedule(models.Model):

    no = models.AutoField(primary_key=True)
    tech_name = models.ForeignKey(Technicians, on_delete=models.PROTECT)
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return f"Flight Schedule {self.no} - {self.tech_name.name}"



