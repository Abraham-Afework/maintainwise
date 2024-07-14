from django.contrib.auth.models import User
from ..models import Technicians, Profile
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import PasswordChangeView
from django.urls import reverse_lazy
from ..forms import CustomPasswordChangeForm

def create_technician_profiles(request):

    default_password='defaultpassword'
    for technician in Technicians.objects.all():

        full_name = technician.name.strip()  # Remove any leading or trailing spaces
        if ' ' in full_name:
            first_name, last_name = full_name.split(maxsplit=1)
        else:
            first_name = full_name
            last_name = ""
        # Check if user already exists
        if User.objects.filter(username=technician.emp_id).exists():
           continue

        # Create user with hashed password

        user = User.objects.create_user(
            username=technician.emp_id,
            password=default_password,
            first_name=first_name,
            last_name=last_name,
        )

        # Create profile
        Profile.objects.create(
            user=user,
            role='employee'  # Assuming default role is 'employee'
        )

def change_password_modal(request):
    form = CustomPasswordChangeForm(request.user)
    return render(request, 'change_password_modal.html', {'form': form})

@login_required
def change_password(request):
    if request.method == 'POST':
        form = CustomPasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # Redirect to profile page after successful password change
        else:
            pass
    else:
        form = CustomPasswordChangeForm(request.user)
    return render(request, 'change_password_form.html', {'form': form})

class MyPasswordChangeView(PasswordChangeView):
    form_class = CustomPasswordChangeForm
    success_url = reverse_lazy('password_change_done')


