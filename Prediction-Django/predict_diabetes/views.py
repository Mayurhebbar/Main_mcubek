import joblib
from django.shortcuts import render
from django.http import JsonResponse
import pandas as pd
from .models import PredResults_diabetes
from sklearn.preprocessing import StandardScaler


def predict_diabetes(request):
    return render(request, 'doctor_template/predict_diabetes.html')


def predict_chances_diabetes(request):
    if request.POST.get('action') == 'post':
        # Receive data from client
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
    
        #Deserialization of objects
        # Unpickle model
        model = joblib.load("diabetes_model")
        result = model.predict(
            [[Pregnancies, Glucose, BloodPressure, SkinThickness,
              Insulin, BMI, DiabetesPedigreeFunction, Patient_Age]])
        
        print(result)

        diabetes_Disease = result[0]
        '''
        if diabetes_Disease == 0:
            disease = "No"
        else:
            disease = "Yes"
        '''

        PredResults_diabetes.objects.create(Patient_ID=Patient_ID, Patient_Age=Patient_Age, Patient_Gender=Patient_Gender,
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
    data = {"dataset": PredResults_diabetes.objects.all()}

    return render(request, "doctor_template/result_diabetes.html", data)