import joblib
from django.shortcuts import render
from django.http import JsonResponse
import pandas as pd
from .models import PredResults
from sklearn.preprocessing import StandardScaler


def predict(request):
    return render(request, 'predict.html')


def predict_chances(request):
    if request.POST.get('action') == 'post':
        # Receive data from client
        Patient_ID = int(request.POST.get('Patient_ID'))
        print("PID", Patient_ID)
        Patient_Age = int(request.POST.get('Patient_Age'))
        print("Page", Patient_Age)
        Patient_Gender = int(request.POST.get('Patient_Gender'))
        print("Pgen", Patient_Gender)
        CP = int(request.POST.get('cp'))
        print("CP = ", CP)
        Trestbps = int(request.POST.get('trestbps'))
        print("trestbps = ", Trestbps)
        Cholesterol = int(request.POST.get('chol'))
        #FBS = int(request.POST.get('fbs'))
        Restecg = int(request.POST.get('restecg'))
        Thalach = int(request.POST.get('thalach'))
        Exang = int(request.POST.get('exang'))
        Oldpeak = float(request.POST.get('oldpeak'))
        Slope = int(request.POST.get('slope'))
        #CA = int(request.POST.get('ca'))
        Thal = int(request.POST.get('thal'))

        # standardizing variables

        sc = StandardScaler()
        Patient_Age1 = sc.fit_transform([[Patient_Age]])
        Patient_Gender1 = sc.fit_transform([[Patient_Gender]])
        CP = sc.fit_transform([[CP]])
        Trestbps = sc.fit_transform([[Trestbps]])
        Cholesterol = sc.fit_transform([[Cholesterol]])
        Restecg = sc.fit_transform([[Restecg]])
        Thalach = sc.fit_transform([[Thalach]])
        Exang = sc.fit_transform([[Exang]])
        Oldpeak = sc.fit_transform([[Oldpeak]])
        Slope = sc.fit_transform([[Slope]])
        Thal = sc.fit_transform([[Thal]])


        # Unpickle model
        model = joblib.load("heart_model")
        # Make prediction
        result = model.predict([[Patient_Age1[0][0], Patient_Gender1[0][0], CP[0][0], Trestbps[0][0], Cholesterol[0][0], Restecg[0][0],
                                 Thalach[0][0], Exang[0][0], Oldpeak[0][0], Slope[0][0], Thal[0][0]]])

        Heart_Disease = result[0]
        print("heart..................",Heart_Disease)

        PredResults.objects.create(Patient_ID=Patient_ID, Patient_Age=Patient_Age, Patient_Gender=Patient_Gender,
                                   Heart_Disease=Heart_Disease)

        return JsonResponse({'result': Heart_Disease, 'Patient_ID': Patient_ID, 'Patient_Age': Patient_Age, 'Patient_Gender': Patient_Gender},
                            safe=False)


def view_results(request):
    # Submit prediction and show all
    data = {"dataset": PredResults.objects.all()}
    return render(request, "results.html", data)
