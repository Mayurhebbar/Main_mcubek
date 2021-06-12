import joblib
from django.shortcuts import render
from django.http import JsonResponse
import pandas as pd
from .models import PredResults
from sklearn.preprocessing import StandardScaler
import numpy as np


def predict_heart(request):
    return render(request, 'doctor_template/predict_heart.html')


def predict_chances_heart(request):
    if request.POST.get('action') == 'post':
        # Receive data from client
        Patient_ID = float(request.POST.get('Patient_ID'))
        Patient_Age = float(request.POST.get('Patient_Age'))
        Patient_Gender = float(request.POST.get('Patient_Gender'))
        CP = float(request.POST.get('cp'))
        Trestbps = float(request.POST.get('trestbps'))
        Cholesterol = float(request.POST.get('chol'))
        # FBS = int(request.POST.get('fbs'))
        Restecg = float(request.POST.get('restecg'))
        Thalach = float(request.POST.get('thalach'))
        Exang = float(request.POST.get('exang'))
        Oldpeak = float(request.POST.get('oldpeak'))
        Slope = float(request.POST.get('slope'))
        # CA = int(request.POST.get('ca'))
        Thal = float(request.POST.get('thal'))

        # standardizing variables
        sc_test=joblib.load("Heart_Standard_Scalar")
        model_test=joblib.load("heart_model")

        #Array Input Ndarray
        array_input=[[Patient_Age,Patient_Gender,CP,Trestbps,Cholesterol,Restecg,Thalach,Exang,Oldpeak,Slope,Thal]]

        #Logging the index variables in the dataframe
        array_input[0][3]=np.log(array_input[0][3])
        array_input[0][4]=np.log(array_input[0][4])

        #Transform the model using the Standard Scalar desreialised object
        array_input=sc_test.transform(array_input)

        #Predict the output using heart_model ML deserialize object
        result=model_test.predict(array_input)

        #Results obtained from the deserialized object(ML object)
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
