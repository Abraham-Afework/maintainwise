from django.contrib.auth.models import User
from django import forms
from .models import MonthYear,Schedule,Faults




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