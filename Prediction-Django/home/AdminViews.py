import datetime

from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.core.files.storage import FileSystemStorage
from home.models import CustomUser, Doctors
from predict_heart.models import PredResults_heart
from predict_cancers.models import PredResults_cancers
from predict_kidney.models import PredResults_kidney
from predict_diabetes.models import PredResults_diabetes
from django.views.decorators.csrf import csrf_exempt


def admin_home(request):
    doctor_count = Doctors.objects.all().count()
    heart_patients = PredResults_heart.objects.all().count()
    diabetes_patients = PredResults_diabetes.objects.all().count()
    kidney_patients = PredResults_kidney.objects.all().count()
    cancer_patients = PredResults_cancers.objects.all().count()
    heart_doctors = Doctors.objects.filter(specialization="Heart").count()
    diabetes_doctors = Doctors.objects.filter(specialization="Diabetes").count()
    kidney_doctors = Doctors.objects.filter(specialization="Kidney").count()
    cancer_doctors = Doctors.objects.filter(specialization="Cancer").count()
    total_patients_count = heart_patients+diabetes_patients+kidney_patients+cancer_patients

    return render(request, "admin_template/admin_main_content.html",
                  {"doctor_count": doctor_count, "heart_patients": heart_patients,
                   "diabetes_patients": diabetes_patients, "total_patients_count": total_patients_count,
                   "kidney_patients": kidney_patients, "cancer_patients": cancer_patients, "heart_doctors": heart_doctors,
                   "diabetes_doctors": diabetes_doctors,
                   "kidney_doctors": kidney_doctors, "cancer_doctors": cancer_doctors
                   })


def add_doctor(request):
    return render(request, "admin_template/add_doctor_template.html")


def add_doctor_save(request):
    if request.method != "POST":
        return HttpResponse("Method Not Allowed")
    else:
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        username = request.POST.get("username")
        email = request.POST.get("email")
        specialization = request.POST.get("specialization")
        dob = request.POST.get("dob")
        blood_group = request.POST.get("blood_group")
        doctor_num = request.POST.get("doctor_num")
        password = request.POST.get("password")
        address = request.POST.get("address")
        gender = request.POST.get("gender")
        ph_no = request.POST.get("ph_no")
        qualification = request.POST.get("qualification")
        profile_pic = request.FILES['profile_pic']
        fs = FileSystemStorage()
        filename = fs.save(profile_pic.name, profile_pic)
        profile_pic_url = fs.url(filename)

        try:
            user = CustomUser.objects.create_user(username=username, password=password, email=email,
                                                  last_name=last_name, first_name=first_name, user_type=2)
            user.doctors.gender = gender
            user.doctors.address = address
            user.doctors.ph_no = ph_no
            user.doctors.dob = dob
            user.doctors.specialization = specialization
            user.doctors.blood_group = blood_group
            user.doctors.doctor_num = doctor_num
            user.doctors.qualification = qualification
            user.doctors.profile_pic = profile_pic_url
            user.save()
            messages.success(request, "Successfully Added Doctor")
            return HttpResponseRedirect(reverse("home:add_doctor"))
        except:
            messages.error(request, "Failed to Add Doctor")
            return HttpResponseRedirect(reverse("home:add_doctor"))


def manage_doctor(request):
    doctors = Doctors.objects.all()
    return render(request, "admin_template/manage_doctor_template.html", {"doctors": doctors})


def edit_doctor(request, doctor_id):
    doctor = Doctors.objects.get(admin=doctor_id)
    return render(request, "admin_template/edit_doctor_template.html", {"doctor": doctor, "id": doctor_id})


def edit_doctor_save(request):
    if request.method != 'POST':
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        doctor_id = request.POST.get("doctor_id")
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        username = request.POST.get("username")
        email = request.POST.get("email")
        dob = request.POST.get("dob")
        specialization = request.POST.get("specialization")
        blood_group = request.POST.get("blood_group")
        address = request.POST.get("address")
        gender = request.POST.get("gender")
        qualification = request.POST.get("qualification")
        ph_no = request.POST.get("ph_no")
        doctor_num = request.POST.get("doctor_num")

        if request.FILES.get('profile_pic', False):
            profile_pic = request.FILES['profile_pic']
            fs = FileSystemStorage()
            filename = fs.save(profile_pic.name, profile_pic)
            profile_pic_url = fs.url(filename)
        else:
            profile_pic_url = None

        try:
            user = CustomUser.objects.get(id=doctor_id)
            user.first_name = first_name
            user.last_name = last_name
            user.username = username
            user.email = email
            user.save()

            doctor_model = Doctors.objects.get(admin=doctor_id)
            doctor_model.address = address
            doctor_model.dob = dob
            doctor_model.specialization = specialization
            doctor_model.blood_group = blood_group
            doctor_model.doctor_num = doctor_num
            doctor_model.qualification = qualification
            if profile_pic_url != None:
                doctor_model.profile_pic = profile_pic_url
            doctor_model.gender = gender
            doctor_model.ph_no = ph_no
            doctor_model.save()
            messages.success(request, "Successfully Updated Doctor Details")
            return HttpResponseRedirect(reverse("home:edit_doctor", kwargs={"doctor_id": doctor_id}))
        except:
            messages.error(request, "Failed to Edit Doctor Details")
            return HttpResponseRedirect(reverse("home:edit_doctor", kwargs={"doctor_id": doctor_id}))


@csrf_exempt
def check_email_exist(request):
    email = request.POST.get("email")
    user_obj = CustomUser.objects.filter(email=email).exists()
    if user_obj:
        return HttpResponse(True)
    else:
        return HttpResponse(False)


@csrf_exempt
def check_doctor_num_exist(request):
    doctor_num = request.POST.get("doctor_num")
    user_obj = Doctors.objects.filter(doctor_num=doctor_num).exists()
    if user_obj:
        return HttpResponse(True)
    else:
        return HttpResponse(False)


@csrf_exempt
def check_username_exist(request):
    username = request.POST.get("username")
    user_obj = CustomUser.objects.filter(username=username).exists()
    if user_obj:
        return HttpResponse(True)
    else:
        return HttpResponse(False)


def delete_doctor(request, doctor_id):
    user = CustomUser.objects.get(id=doctor_id)
    user.delete()
    return HttpResponseRedirect(reverse("home:manage_doctor"))


def admin_profile(request):
    user = CustomUser.objects.get(id=request.user.id)
    return render(request, "admin_template/admin_profile.html", {"user": user})


def admin_profile_save(request):
    if request.method != "POST":
        return HttpResponseRedirect(reverse("home:admin_profile"))
    else:
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        password = request.POST.get("password")
        try:
            customuser = CustomUser.objects.get(id=request.user.id)
            customuser.first_name = first_name
            customuser.last_name = last_name
            if password != None and password != "":
                customuser.set_password(password)
            customuser.save()
            messages.success(request, "Successfully Updated Profile")
            return HttpResponseRedirect(reverse("home:admin_profile"))
        except:
            messages.error(request, "Failed to Update Profile")
            return HttpResponseRedirect(reverse("home:admin_profile"))
