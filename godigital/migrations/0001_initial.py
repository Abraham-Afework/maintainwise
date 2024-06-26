# Generated by Django 3.2.6 on 2024-06-26 21:30

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Aircrafts',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('aircraft_reg', models.CharField(max_length=100)),
                ('fleet', models.CharField(choices=[('B777', 'Boeing 777'), ('B787', 'Boeing 787'), ('B737', 'Boeing 737'), ('B767', 'Boeing 767'), ('A350', 'Airbus A350'), ('Q400', 'Bombardier Q400')], max_length=4)),
            ],
        ),
        migrations.CreateModel(
            name='MonthYear',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='Technicians',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('emp_id', models.CharField(max_length=10)),
                ('position', models.CharField(max_length=100)),
                ('fleet', models.CharField(max_length=10, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='FlightSchedule',
            fields=[
                ('no', models.AutoField(primary_key=True, serialize=False)),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('tech_name', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='godigital.technicians')),
            ],
        ),
        migrations.CreateModel(
            name='Faults',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('faults', models.TextField()),
                ('action_taken', models.TextField(blank=True, null=True)),
                ('found_date', models.DateField()),
                ('status', models.CharField(choices=[('OPEN', 'Open'), ('IN_PROGRESS', 'In Progress'), ('RESOLVED', 'Resolved'), ('CLOSED', 'Closed')], default='OPEN', max_length=20, null=True)),
                ('aircraft', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='godigital.aircrafts')),
                ('created_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='godigital.technicians')),
            ],
        ),
        migrations.CreateModel(
            name='Scheduledate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(default=datetime.datetime(2024, 6, 26, 21, 30, 41, 877037))),
                ('shift', models.CharField(blank=True, choices=[('M', 'Morning'), ('E', 'Evening'), ('N', 'Night'), ('FT', 'Flight'), ('TR', 'Training'), ('V', 'Vaccation')], max_length=10, null=True)),
                ('is_day_off', models.BooleanField(default=False)),
                ('technician', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='godigital.technicians')),
            ],
            options={
                'unique_together': {('technician', 'date', 'shift')},
            },
        ),
        migrations.CreateModel(
            name='Schedule',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('shift', models.CharField(max_length=10)),
                ('dayoff', models.CharField(choices=[('Mon-Tue', 'Mon-Tue'), ('Tue-Wed', 'Tue-Wed'), ('Wed-Thu', 'Wed-Thu'), ('Thu-Fri', 'Thu-Fri'), ('Fri-Sat', 'Fri-Sat'), ('Sat-Sun', 'Sat-Sun'), ('Sun-Mon', 'Sun-Mon')], max_length=8)),
                ('date', models.DateField(null=True)),
                ('month', models.IntegerField(choices=[(1, 'Jan'), (2, 'Feb'), (3, 'Mar'), (4, 'Apr'), (5, 'May'), (6, 'Jun'), (7, 'Jul'), (8, 'Aug'), (9, 'Sep'), (10, 'Oct'), (11, 'Nov'), (12, 'Dec')])),
                ('year', models.IntegerField(choices=[(2024, 2024), (2025, 2025), (2026, 2026), (2027, 2027), (2028, 2028), (2029, 2029), (2030, 2030), (2031, 2031), (2032, 2032), (2033, 2033)])),
                ('technician', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='godigital.technicians')),
            ],
            options={
                'unique_together': {('technician', 'month', 'year')},
            },
        ),
    ]
