import datetime

from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from home.models import CustomUser, Doctors


def doctor_home(request):
    return render(request, "doctor_template/doctor_main_content.html")


def doctor_profile(request):
    user = CustomUser.objects.get(id=request.user.id)
    doctor = Doctors.objects.get(admin=user)
    return render(request, "doctor_template/doctor_profile.html", {"user": user, "doctor": doctor})


def doctor_profile_save(request):
    if request.method != "POST":
        return HttpResponseRedirect(reverse("home:doctor_profile"))
    else:
        '''
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        address = request.POST.get("address")   
        ph_no = request.POST.get("ph_no")
        gender = request.POST.get("gender")
        '''
        password = request.POST.get("password")
        try:
            customuser = CustomUser.objects.get(id=request.user.id)
            '''
            customuser.first_name = first_name
            customuser.last_name = last_name
            '''
            if password != None and password != "":
                customuser.set_password(password)
            customuser.save()
            '''
            doctor = Doctors.objects.get(admin=customuser.id)
            doctor.address = address
            doctor.gender = gender
            doctor.ph_no = ph_no
            doctor.save()
            '''
            messages.success(request, "Successfully Updated Password")
            return HttpResponseRedirect(reverse("home:doctor_profile"))
        except:
            messages.error(request, "Failed to Update Password")
            return HttpResponseRedirect(reverse("home:doctor_profile"))
