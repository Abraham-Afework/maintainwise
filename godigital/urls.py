from django.urls import path
# from posts import views
from .views import digital_resume_views,views,miscellaneous_view,daily_assignment_view,customer_handling_view, account_view


urlpatterns = [

    # path('change-password/', account_view.change_password, name='change_password'),
    # path('change-password-class/', account_view.MyPasswordChangeView.as_view, name='change_password_class'),

    path('change-password/', account_view.change_password_modal, name='change_password_modal'),
    path('change-password/submit/', account_view.change_password, name='change_password'),




	path('',views.index, name='index'),

	path('test/',views.test, name='test'),
	path('add/',views.add_tech, name='add'),
	path('register/',views.register, name='register'),
    path('create-profiles/',account_view.create_technician_profiles, name='create_profiles'),
	path('login/',views.login_view, name='login'),
	path('logout/',views.logout_view, name='logout'),
	path('all_tech/',views.all_tech, name='all_tech'),
	path('monthly_schedule/',views.new_monthly_schedule, name='monthly_schedule'),
	path('formset/',views.add_formset, name='add_formset'),

# 	path('new_monthly_schedule/',views.new_monthly_schedule, name='new_monthly_schedule'),
	path('start_schedule/',views.schedule_create, name='start_schedule'),
	path('get_employee_name/',views.get_employee_name, name='get_employee_name'),
    path('edit_schedule/<int:emp_id>/<int:month>/<int:year>/', views.edit_schedule, name='edit_schedule'),
    path('schedule_creater/', views.schedule_create_or_edit, name='schedule_creater'),
    path('schedule/edit/<int:emp_id>/', views.schedule_create_or_edit, name='schedule_edit'),


    path('schedule/confirm_delete/<int:emp_id>/<int:month>/<int:year>/', views.confirm_delete_schedule, name='confirm_delete_schedule'),
    path('schedule/delete/<int:emp_id>/<int:month>/<int:year>/', views.delete_schedule, name='delete_schedule'),


    path('schedule/delete/<int:emp_id>/<int:month>/<int:year>/', views.delete_schedule, name='delete_schedule'),

    # path('export/', views.export_schedule_to_excel, name='export_schedule_to_excel'),
    path('search_schedule/',views.search_schedule, name='search_schedule'),
    path('schedule_create/',views.schedule_create, name='schedule_create'),
    path('schedule_create_batch/',views.schedule_create_batch, name='schedule_create_batch'),
    path('schedule_form_template/', views.schedule_form_template, name='schedule_form_template'),






    path('digital_resume/', digital_resume_views.digital_resume, name='digital_resume'),
    path('add_resume/', digital_resume_views.add_digital_resume, name='add_resume'),
    path('get_aircraft_name/',digital_resume_views.get_aircraft_name, name='get_aircraft_name'),
    path('get-faults/', digital_resume_views.get_faults, name='get_faults'),


    path('flight_schedule/', miscellaneous_view.flight_schedule, name='flight_schedule'),
    path('add_flight_schedule/', miscellaneous_view.add_flight_schedule, name='add_flight_schedule'),





    path('daily_assignment/', daily_assignment_view.daily_assignment, name='daily_assignment'),

    path('log_list', customer_handling_view.log_list, name='log_list'),
    path('create/', customer_handling_view.log_create, name='log_create'),
    path('operator_airline/', customer_handling_view.operator_airline, name='operator_airline'),
    path('load-reg-numbers/', customer_handling_view.load_reg_numbers, name='load_reg_numbers'),
    path('export_to_excel/', customer_handling_view.export_to_excel, name='export_to_excel'),













]




# handler404 = 'blog.views.custom_404_view'