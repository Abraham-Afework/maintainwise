from django.contrib.auth.models import User
from django import forms
from django.contrib.auth.forms import PasswordChangeForm
from .models import MonthYear,Schedule,Faults,ServiceLog,OperatorAirline,Aircrafts
from django.forms import formset_factory
from datetime import date, time
from django.urls import reverse_lazy





class LoginForm(forms.ModelForm):

	password = forms.CharField(widget=forms.PasswordInput)

	class Meta:
		model=User
		fields=['username','password']


class RegistrationForm(forms.ModelForm):
	password = forms.CharField(widget=forms.PasswordInput)

	class Meta:
		model= User
		fields=['username','email','password','first_name','last_name']





class CustomPasswordChangeForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Customize form labels or attributes if needed
        self.fields['old_password'].label = 'Current Password'
        self.fields['new_password1'].label = 'New Password'
        self.fields['new_password2'].label = 'Confirm New Password'


class MonthYearForm(forms.ModelForm):
    date = forms.DateField(widget=forms.DateInput(attrs={'type': 'month'}))

    class Meta:
        model = MonthYear
        fields = ['date']

class Add_ScheduleForm(forms.ModelForm):

    emp_id = forms.CharField(max_length=100)
    # name = forms.CharField(max_length=100)
    shift = forms.CharField(max_length=100)
    dayoff = forms.CharField(max_length=20)
    # month = forms.IntegerField()  # Assuming month will be an integer field
    # year = forms.IntegerField()   # Assuming year will be an integer field

    class Meta:
        model = Schedule
        fields = ['emp_id', 'shift', 'dayoff', 'month', 'year']

class FaultForm(forms.ModelForm):
    class Meta:
        model = Faults
        # fields = ['aircraft', 'faults', 'action_taken', 'found_date', 'status', 'created_by']
        fields = ['aircraft','faults', 'action_taken','found_date',]

        widgets = {
            'faults': forms.TextInput(attrs={'class': 'form-control'}),
            'action_taken': forms.Textarea(attrs={'class': 'form-control', 'rows': 1}),
            'found_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),

        }


class ScheduleForm(forms.Form):
    emp_id = forms.ChoiceField(choices=[])  # We will populate choices in the view
    start_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    end_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    shift = forms.ChoiceField(choices=[
        ("M", "Morning"),
        ("LM", "Late Morning"),
        ("O", "Office Hour"),
        ("E", "Evening"),
        ("LE", "Late Evening"),
        ("Night", "Night"),
        ("V", "Vacation"),
        ("FT", "Flight"),
        ("TR", "Training"),
        ("CH", "Coaching")
    ])
    day_off = forms.ChoiceField(choices=[
        ("Mon-Tue", "Mon-Tue"),
        ("Tue-Wed", "Tue-Wed"),
        ("Wed-Thu", "Wed-Thu"),
        ("Thu-Fri", "Thu-Fri"),
        ("Fri-Sat", "Fri-Sat"),
        ("Sat-Sun", "Sat-Sun"),
        ("Sun-Mon", "Sun-Mon")
    ])

# Use formset_factory to create a formset
ScheduleFormSet = formset_factory(ScheduleForm, extra=1)


class ServiceLogForm(forms.ModelForm):

    operator_airline = forms.ModelChoiceField(
        queryset=OperatorAirline.objects.all().order_by('airline_name'),
        widget=forms.Select(attrs={
            'class': 'selectpicker',
            'data-style': 'btn-default',
            'data-live-search': 'true',
            'placeholder': 'Select an operator airline',
            'hx-get': reverse_lazy('load_reg_numbers'),  # URL to fetch reg numbers based on selected operator
            'hx-trigger': 'change',
            'hx-target': '#id_reg_no'
        })
    )

    reg_no = forms.ModelChoiceField(queryset=Aircrafts.objects.all(), required=True,
                                    widget=forms.Select(attrs={
                                        'class': 'selectpicker',
                                        'data-style': 'btn-default',
                                        'data-live-search': 'true',
                                        'id': 'id_reg_no',
                                        'placeholder': 'Select registration number'
                                    }))

    class Meta:
        model = ServiceLog
        fields = '__all__'
        widgets = {
            'date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date', 'placeholder': 'Select date'}),
            'aircraft_type': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter aircraft type'}),
            'reg_no': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter registration number'}),
            'remarks':forms.Textarea(attrs={'class': 'form-control', 'rows': '1','height': '38px;','placeholder': 'Enter remarks'}),
            'flt_no': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter flight number'}),
            'svc_chk_action_taken': forms.Textarea(attrs={'class': 'form-control', 'rows': '1', 'height': '38px;','placeholder': 'Enter service check/action taken'}),
            'arr_time': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time', 'placeholder': 'Enter arrival time'}),
            'dep_time': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time', 'placeholder': 'Enter departure time'}),

        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['date'].initial = date.today()
        self.fields['aircraft_type'].initial = 'B777-300'
        self.fields['reg_no'].initial = 'A6-EGR'
        self.fields['flt_no'].initial = 'EK-724'
        self.fields['svc_chk_action_taken'].initial = 'PRE-FLIGHT CHECK'
        self.fields['arr_time'].initial = time(11, 0)  # Default to 11:00 AM
        self.fields['dep_time'].initial = time(14, 0)  # Default to 2:00 PM
        self.fields['operator_airline'].initial = 'select airline'  # Assuming None is acceptable if not required
        # try:
        #     emirates = OperatorAirline.objects.get(airline_name="Emirates")
        #     self.fields['operator_airline'].initial = emirates.id
        # except OperatorAirline.DoesNotExist:
        #     pass  # Handle the case where Emirates