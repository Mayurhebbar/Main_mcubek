from django.urls import path, include
from . import views
from home import AdminViews, DoctorViews

app_name = "home"

urlpatterns = [
    #path('accounts/', include('django.contrib.auth.urls')),
    path('', views.ShowLoginPage, name="show_login"),
    path('doLogin', views.doLogin, name="do_login"),
    path('logout_user', views.logout_user, name="logout"),
    path('get_user_details', views.GetUserDetails),
    path('add_doctor', AdminViews.add_doctor, name="add_doctor"),
    path('add_doctor_save', AdminViews.add_doctor_save, name="add_doctor_save"),
    path('manage_doctor', AdminViews.manage_doctor, name="manage_doctor"),
    path('edit_doctor/<str:doctor_id>', AdminViews.edit_doctor, name="edit_doctor"),
    path('edit_doctor_save', AdminViews.edit_doctor_save, name="edit_doctor_save"),
    path('check_email_exist', AdminViews.check_email_exist, name="check_email_exist"),
    path('check_doctor_num_exist', AdminViews.check_doctor_num_exist, name="check_doctor_num_exist"),
    path('check_username_exist', AdminViews.check_username_exist, name="check_username_exist"),
    path('delete_doctor/<str:doctor_id>', AdminViews.delete_doctor, name="delete_doctor"),
    path('admin_profile', AdminViews.admin_profile, name="admin_profile"),
    path('admin_profile_save', AdminViews.admin_profile_save, name="admin_profile_save"),
    path('doctor_profile', DoctorViews.doctor_profile, name="doctor_profile"),
    path('doctor_profile_save', DoctorViews.doctor_profile_save, name="doctor_profile_save"),
    path('admin_home', AdminViews.admin_home, name="admin_home"),
    path('doctor_home', DoctorViews.doctor_home, name="doctor_home"),


]