import joblib
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
import pandas as pd
from .models import PredResults_diabetes
from home.models import CustomUser, Doctors
from sklearn.preprocessing import StandardScaler
import numpy as np
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa

def predict_diabetes_render_pdf_view(request, *args, **kwargs):
    Patient_ID = kwargs.get('Patient_ID')
    predict_diabetes = get_object_or_404(PredResults_diabetes, Patient_ID=Patient_ID)
    doctor_details = get_object_or_404(CustomUser, id=request.user.id)
    doctor_details_new = get_object_or_404(Doctors, admin_id=request.user.id)
    template_path = 'predict_diabetes/pdf2.html'
    context = {'predict_diabetes': predict_diabetes, 'doctor_details': doctor_details, 'doctor_details_new': doctor_details_new}
    # Create a Django response object, and specify content_type as pdf
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="Diabetes Disease Report.pdf"'
    # find the template and render it.
    template = get_template(template_path)
    print(template)
    html = template.render(context)

    # create a pdf
    pisa_status = pisa.CreatePDF(
        html, dest=response)
    # if error then show some funy view
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response


def predict_diabetes(request):
    return render(request, 'doctor_template/predict_diabetes.html')


def predict_chances_diabetes(request):
    if request.POST.get('action') == 'post':
        # Receive data from client
        Patient_Name = str(request.POST.get('Patient_Name'))
        Patient_ID = float(request.POST.get('Patient_ID'))
        Patient_Age = float(request.POST.get('Patient_Age'))
        Patient_Gender = float(request.POST.get('Patient_Gender'))
        Pregnancies = float(request.POST.get('pregnancies'))
        Glucose = float(request.POST.get('glucose'))
        BloodPressure = float(request.POST.get('bloodPressure'))
        SkinThickness = float(request.POST.get('skinThickness'))
        Insulin = float(request.POST.get('insulin'))
        BMI = float(request.POST.get('bmi'))
        DiabetesPedigreeFunction = float(request.POST.get('diabetesPedigreeFunction'))
        consulted_doctor = request.user.id
    
        #Deserialization of objects
        # Unpickle model
        model = joblib.load("diabetes_model")
        
        result = model.predict(
            [[Pregnancies, Glucose, BloodPressure, SkinThickness,
              Insulin, BMI, DiabetesPedigreeFunction, Patient_Age]])
        
        probability = model.predict_proba([[Pregnancies, Glucose, BloodPressure, SkinThickness,
              Insulin, BMI, DiabetesPedigreeFunction, Patient_Age]])

        probab_perc=round(probability[0][1]*100,3)

        print(probab_perc)

        Diabetes_Disease = result[0]

        if Diabetes_Disease == 0:
            disease = "No Risk"
        else:
            disease = "At Risk"

        patients_lists = PredResults_diabetes.objects.all()
        ID_list = []
        for patients_list in patients_lists:
            individual_list = patients_list.Patient_ID
            ID_list.append(individual_list)

        if Patient_ID not in ID_list:
            user = PredResults_diabetes(Patient_ID=Patient_ID, Patient_Name=Patient_Name, Patient_Age=Patient_Age,
                                       Patient_Gender=Patient_Gender,
                                       Diabetes_Disease=Diabetes_Disease, Pregnancies=Pregnancies, Glucose=Glucose, BloodPressure=BloodPressure,
                                       SkinThickness=SkinThickness, Insulin=Insulin,
                                       BMI=BMI, DiabetesPedigreeFunction=DiabetesPedigreeFunction, consulted_doctor=consulted_doctor)
            user.save()
        else:
            update_list = PredResults_diabetes.objects.get(Patient_ID=Patient_ID)
            update_list.Patient_Age = Patient_Age
            update_list.Diabetes_Disease = Diabetes_Disease
            update_list.Pregnancies = Pregnancies
            update_list.Glucose = Glucose
            update_list.BloodPressure = BloodPressure
            update_list.SkinThickness = SkinThickness
            update_list.Insulin = Insulin
            update_list.BMI = BMI
            update_list.DiabetesPedigreeFunction = DiabetesPedigreeFunction
            update_list.consulted_doctor = consulted_doctor
            update_list.save()
        if Patient_Gender == 0:
            Patient_Gender = "Female"
        else:
            Patient_Gender = "Male"

        if Glucose < 120:
            Glucose = "Normal"
        else:
            Glucose = "Diabetic"

        if SkinThickness < 15:
            SkinThickness = "Normal"
        elif SkinThickness > 15 and SkinThickness < 30:
            SkinThickness = "Moderate Risk"
        else:
            SkinThickness = "Risk is High for Occurance of Diabetes"

        if Insulin < 100:
            Insulin = "Normal"
        elif Insulin > 100 and Insulin < 300:
            Insulin = "Lessely Occuring"
        else:
            Insulin = "Diabetic"

        if BMI < 25:
            BMI = "Normal"
        else:
            BMI = "Over Weight-Risk is High for Occurance of Diabetes"

        return JsonResponse({'result': disease, 'Patient_ID': Patient_ID, 'Patient_Age': Patient_Age, 'Patient_Name': Patient_Name,
                             'Patient_Gender': Patient_Gender, 'pregnancies': Pregnancies, 'glucose': Glucose, 'bloodPressure': BloodPressure,
                             'skinThickness': SkinThickness, 'insulin': Insulin, 'bmi': BMI, 'diabetesPedigreeFunction': DiabetesPedigreeFunction
                            },
                            safe=False)


def view_results_diabetes(request):
    # Submit prediction and show all
    data = {"dataset": PredResults_diabetes.objects.all()}

    return render(request, "doctor_template/result_diabetes.html", data)