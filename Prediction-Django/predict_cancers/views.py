import joblib
from django.shortcuts import render
from django.http import JsonResponse
import pandas as pd
from .models import PredResults_cancers
from sklearn.preprocessing import StandardScaler


def predict_cancer(request):
    return render(request, 'doctor_template/predict_cancers.html')


def predict_chances_cancer(request):
    if request.POST.get('action') == 'post':
        # Receive data from client
        Patient_ID = float(request.POST.get('Patient_ID'))
        Patient_Age = float(request.POST.get('Patient_Age'))
        Patient_Gender = float(request.POST.get('Patient_Gender'))
        Radius_Mean = float(request.POST.get('radius_mean'))
        Texture_Mean = float(request.POST.get('texture_mean'))
        Perimeter_Mean = float(request.POST.get('perimeter_mean'))
        Area_Mean = float(request.POST.get('area_mean'))
        Smoothness_Mean = float(request.POST.get('smoothness_mean'))
        Compactness_Mean = float(request.POST.get('compactness_mean'))
        Concavity_Mean = float(request.POST.get('concavity_mean'))
        Concave_Points_Mean = float(request.POST.get('concave_points_mean'))
        Symmetry_Mean = float(request.POST.get('symmetry_mean'))
        Fractal_Dimension_Mean = float(request.POST.get('fractal_dimension_mean'))
        Radius_Se = float(request.POST.get('radius_se'))
        Texture_Se = float(request.POST.get('texture_se'))
        Perimeter_Se = float(request.POST.get('perimeter_se'))
        Area_Se = float(request.POST.get('area_se'))
        Smoothness_Se = float(request.POST.get('smoothness_se'))
        Compactness_Se = float(request.POST.get('compactness_se'))
        Concavity_Se = float(request.POST.get('concavity_se'))
        Concave_Points_Se = float(request.POST.get('concave_points_se'))
        Symmetry_Se = float(request.POST.get('symmetry_se'))
        Fractal_Dimension_Se = float(request.POST.get('fractal_dimension_se'))
        Radius_Worst = float(request.POST.get('radius_worst'))
        Texture_Worst = float(request.POST.get('texture_worst'))
        Perimeter_Worst = float(request.POST.get('perimeter_worst'))
        Area_Worst = float(request.POST.get('area_worst'))
        Smoothness_Worst = float(request.POST.get('smoothness_worst'))
        Compactness_Worst = float(request.POST.get('compactness_worst'))
        Concavity_Worst = float(request.POST.get('concavity_worst'))
        Concave_Points_Worst = float(request.POST.get('concave_points_worst'))
        Symmetry_Worst = float(request.POST.get('symmetry_worst'))
        Fractal_Dimension_Worst = float(request.POST.get('fractal_dimension_worst'))

        #Deserailize the joblib object and READY TO PREDICT THE RESULT
        # Unpickle model
        model = joblib.load("Cancers_model")
        result = model.predict(
            [[ Radius_Mean, Texture_Mean, Perimeter_Mean, Area_Mean,
              Smoothness_Mean, Compactness_Mean, Concavity_Mean, Concave_Points_Mean, Symmetry_Mean, Fractal_Dimension_Mean, Radius_Se, Texture_Se,
              Perimeter_Se, Area_Se, Smoothness_Se, Compactness_Se, Concavity_Se, Concave_Points_Se, Symmetry_Se, Fractal_Dimension_Se,
              Radius_Worst, Texture_Worst, Perimeter_Worst, Area_Worst, Smoothness_Worst, Compactness_Worst, Concavity_Worst, Concave_Points_Worst,
              Symmetry_Worst, Fractal_Dimension_Worst]])

        Cancer_Disease = result[0]
        '''
        if Heart_Disease == 0:
            disease = "No"
        else:
            disease = "Yes"
        '''

        PredResults_cancers.objects.create(Patient_ID=Patient_ID, Patient_Age=Patient_Age, Patient_Gender=Patient_Gender,
                                   Cancer_Disease=Cancer_Disease)
        '''
        if Patient_Gender == 0:
            gender = "Female"
        else:
            gender = "Male"
        '''
        return JsonResponse({'result': int(Cancer_Disease), 'Patient_ID': Patient_ID, 'Patient_Age': Patient_Age,
                             'Patient_Gender': Patient_Gender, 'radius_mean': Radius_Mean, 'texture_mean': Texture_Mean, 'perimeter_mean': Perimeter_Mean,
                             'area_mean': Area_Mean, 'smoothness_mean': Smoothness_Mean, 'compactness_mean': Compactness_Mean, 'concavity_mean': Concavity_Mean,'concave_points_mean': Concave_Points_Mean, 'symmetry_mean': Symmetry_Mean,
                             'fractal_dimension_mean': Fractal_Dimension_Mean, 'radius_se': Radius_Se, 'texture_se': Texture_Se, 'perimeter_se': Perimeter_Se,
                             'area_se': Area_Se, 'smoothness_se': Smoothness_Se, 'compactness_se': Compactness_Se, 'concavity_se': Concavity_Se,
                             'concave_points_se': Concave_Points_Se, 'symmetry_se': Symmetry_Se, 'fractal_dimension_se': Fractal_Dimension_Se, 'radius_worst': Radius_Worst,
                             'texture_worst': Texture_Worst, 'perimeter_worst': Perimeter_Worst, 'area_worst': Area_Worst, 'smoothness_worst': Smoothness_Worst,
                             'compactness_worst': Compactness_Worst, 'concavity_worst': Concavity_Worst, 'concave_points_worst': Concave_Points_Worst, 'symmetry_worst': Symmetry_Worst,
                             'fractal_dimension_worst': Fractal_Dimension_Worst},
                            safe=False)


def view_results_cancer(request):
    # Submit prediction and show all
    data = {"dataset": PredResults_cancers.objects.all()}

    return render(request, "doctor_template/results_cancers.html", data)

