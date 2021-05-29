import joblib
from django.shortcuts import render
from django.http import JsonResponse
import pandas as pd
from .models import PredResults
from sklearn.preprocessing import StandardScaler


def predict_diabetes(request):
    return render(request, 'doctor_template/predict_diabetes.html')


def predict_chances_diabetes(request):
    if request.POST.get('action') == 'post':
        # Receive data from client
        Patient_ID = int(request.POST.get('Patient_ID'))
        Patient_Age = int(request.POST.get('Patient_Age'))
        Patient_Gender = int(request.POST.get('Patient_Gender'))
        Pregnancies = int(request.POST.get('pregnancies'))
        Glucose = int(request.POST.get('glucose'))
        BloodPressure = int(request.POST.get('bloodPressure'))
        # FBS = int(request.POST.get('fbs'))
        SkinThickness = int(request.POST.get('skinThickness'))
        Insulin = int(request.POST.get('insulin'))
        BMI = float(request.POST.get('bmi'))
        DiabetesPedigreeFunction = float(request.POST.get('diabetesPedigreeFunction'))
    
        # standardizing variables

        sc = StandardScaler()
        Patient_Age1 = sc.fit_transform([[Patient_Age]])
        Pregnancies1 = sc.fit_transform([[Pregnancies]])
        Glucose1 = sc.fit_transform([[Glucose]])
        BloodPressure1 = sc.fit_transform([[BloodPressure]])
        SkinThickness1 = sc.fit_transform([[SkinThickness]])
        Insulin1 = sc.fit_transform([[Insulin]])
        BMI1 = sc.fit_transform([[BMI]])
        DiabetesPedigreeFunction1 = sc.fit_transform([[DiabetesPedigreeFunction]])
    
        # Unpickle model
        model = joblib.load("diabetes_model")
        result = model.predict(
            [[Patient_Age1[0][0], Pregnancies1[0][0], Glucose1[0][0], BloodPressure1[0][0], SkinThickness1[0][0],
              Insulin1[0][0], BMI1[0][0], DiabetesPedigreeFunction1[0][0]]])

        diabetes_Disease = result[0]
        '''
        if diabetes_Disease == 0:
            disease = "No"
        else:
            disease = "Yes"
        '''

        PredResults.objects.create(Patient_ID=Patient_ID, Patient_Age=Patient_Age, Patient_Gender=Patient_Gender,
                                   Diabetes_Disease=diabetes_Disease)
        '''
        if Patient_Gender == 0:
            gender = "Female"
        else:
            gender = "Male"
        '''

        return JsonResponse({'result': int(diabetes_Disease), 'Patient_ID': Patient_ID, 'Patient_Age': Patient_Age,
                             'Patient_Gender': Patient_Gender, 'pregnancies': Pregnancies, 'glucose': Glucose, 'bloodPressure': BloodPressure,
                             'skinThickness': SkinThickness, 'insulin': Insulin, 'bmi': BMI, 'diabetesPedigreeFunction': DiabetesPedigreeFunction
                            },
                            safe=False)


def view_results_diabetes(request):
    # Submit prediction and show all
    data = {"dataset": PredResults.objects.all()}

    return render(request, "doctor_template/result_diabetes.html", data)