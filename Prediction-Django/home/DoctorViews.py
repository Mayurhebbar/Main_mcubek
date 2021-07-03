import datetime

from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from home.models import CustomUser, Doctors
from predict_heart.models import PredResults_heart
from predict_cancers.models import PredResults_cancers
from predict_kidney.models import PredResults_kidney
from predict_diabetes.models import PredResults_diabetes


def doctor_home(request):
    doctor_details = Doctors.objects.get(admin_id=request.user.id)
    heart_patients = PredResults_heart.objects.all().count()
    diabetes_patients = PredResults_diabetes.objects.all().count()
    kidney_patients = PredResults_kidney.objects.all().count()
    cancer_patients = PredResults_cancers.objects.all().count()
    heart_patients_under_me = PredResults_heart.objects.filter(consulted_doctor=request.user.id).count()
    diabetes_patients_under_me = PredResults_diabetes.objects.filter(consulted_doctor=request.user.id).count()
    kidney_patients_under_me = PredResults_kidney.objects.filter(consulted_doctor=request.user.id).count()
    cancer_patients_under_me = PredResults_cancers.objects.filter(consulted_doctor=request.user.id).count()
    return render(request, "doctor_template/doctor_main_content.html",
                  {"heart_patients": heart_patients, "diabetes_patients": diabetes_patients,
                   "kidney_patients": kidney_patients, "cancer_patients": cancer_patients,
                   "heart_patients_under_me": heart_patients_under_me,
                   "diabetes_patients_under_me": diabetes_patients_under_me,
                   "kidney_patients_under_me": kidney_patients_under_me,
                   "cancer_patients_under_me": cancer_patients_under_me, "doctor_details": doctor_details
                   })


def doctor_profile(request):
    user = CustomUser.objects.get(id=request.user.id)
    doctor = Doctors.objects.get(admin=user)
    doctor_details = Doctors.objects.get(admin_id=request.user.id)
    return render(request, "doctor_template/doctor_profile.html", {"user": user, "doctor": doctor, "doctor_details": doctor_details})


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
