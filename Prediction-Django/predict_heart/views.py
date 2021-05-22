import joblib
from django.shortcuts import render
from django.http import JsonResponse
import pandas as pd
from .models import PredResults
from sklearn.preprocessing import StandardScaler


def predict_heart(request):
    return render(request, 'doctor_template/predict_heart.html')


def predict_chances_heart(request):
    if request.POST.get('action') == 'post':
        # Receive data from client
        Patient_ID = int(request.POST.get('Patient_ID'))
        Patient_Age = int(request.POST.get('Patient_Age'))
        Patient_Gender = int(request.POST.get('Patient_Gender'))
        CP = int(request.POST.get('cp'))
        Trestbps = int(request.POST.get('trestbps'))
        Cholesterol = int(request.POST.get('chol'))
        # FBS = int(request.POST.get('fbs'))
        Restecg = int(request.POST.get('restecg'))
        Thalach = int(request.POST.get('thalach'))
        Exang = int(request.POST.get('exang'))
        Oldpeak = float(request.POST.get('oldpeak'))
        Slope = int(request.POST.get('slope'))
        # CA = int(request.POST.get('ca'))
        Thal = int(request.POST.get('thal'))

        # standardizing variables

        sc = StandardScaler()
        Patient_Age1 = sc.fit_transform([[Patient_Age]])
        Patient_Gender1 = sc.fit_transform([[Patient_Gender]])
        CP1 = sc.fit_transform([[CP]])
        Trestbps1 = sc.fit_transform([[Trestbps]])
        Cholesterol1 = sc.fit_transform([[Cholesterol]])
        Restecg1 = sc.fit_transform([[Restecg]])
        Thalach1 = sc.fit_transform([[Thalach]])
        Exang1 = sc.fit_transform([[Exang]])
        Oldpeak1 = sc.fit_transform([[Oldpeak]])
        Slope1 = sc.fit_transform([[Slope]])
        Thal1 = sc.fit_transform([[Thal]])

        # Unpickle model
        model = joblib.load("heart_model")
        result = model.predict(
            [[Patient_Age1[0][0], Patient_Gender1[0][0], CP1[0][0], Trestbps1[0][0], Cholesterol1[0][0], Restecg1[0][0],
              Thalach1[0][0], Exang1[0][0], Oldpeak1[0][0], Slope1[0][0], Thal1[0][0]]])

        Heart_Disease = result[0]
        '''
        if Heart_Disease == 0:
            disease = "No"
        else:
            disease = "Yes"
        '''

        PredResults.objects.create(Patient_ID=Patient_ID, Patient_Age=Patient_Age, Patient_Gender=Patient_Gender,
                                   Heart_Disease=Heart_Disease)
        '''
        if Patient_Gender == 0:
            gender = "Female"
        else:
            gender = "Male"
        '''

        return JsonResponse({'result': int(Heart_Disease), 'Patient_ID': Patient_ID, 'Patient_Age': Patient_Age,
                             'Patient_Gender': Patient_Gender, 'cp': CP, 'trestbps': Trestbps, 'chol': Cholesterol,
                             'restecg': Restecg, 'thalach': Thalach, 'exang': Exang, 'oldpeak': Oldpeak, 'slope': Slope,
                             'thal': Thal},
                            safe=False)


def view_results_heart(request):
    # Submit prediction and show all
    data = {"dataset": PredResults.objects.all()}

    return render(request, "doctor_template/results_heart.html", data)
