import joblib
from django.shortcuts import render
from django.http import JsonResponse
import pandas as pd
from .models import PredResults
from sklearn.preprocessing import StandardScaler


def predict_cancer(request):
    return render(request, 'doctor_template/predict_cancers.html')


def predict_chances_cancer(request):
    if request.POST.get('action') == 'post':
        # Receive data from client
        Patient_ID = int(request.POST.get('Patient_ID'))
        Patient_Age = int(request.POST.get('Patient_Age'))
        Patient_Gender = int(request.POST.get('Patient_Gender'))
        Radius_Mean = int(request.POST.get('radius_mean'))
        Texture_Mean = int(request.POST.get('texture_mean'))
        Perimeter_Mean = int(request.POST.get('perimeter_mean'))
        Area_Mean = int(request.POST.get('area_mean'))
        Smoothness_Mean = int(request.POST.get('smoothness_mean'))
        Compactness_Mean = int(request.POST.get('compactness_mean'))
        Concavity_Mean = int(request.POST.get('concavity_mean'))
        Concave_Points_Mean = int(request.POST.get('concave_points_mean'))
        Symmetry_Mean = int(request.POST.get('symmetry_mean'))
        Fractal_Dimension_Mean = int(request.POST.get('fractal_dimension_mean'))
        Radius_Se = int(request.POST.get('radius_se'))
        Texture_Se = int(request.POST.get('texture_se'))
        Perimeter_Se = int(request.POST.get('perimeter_se'))
        Area_Se = int(request.POST.get('area_se'))
        Smoothness_Se = int(request.POST.get('smoothness_se'))
        Compactness_Se = int(request.POST.get('compactness_se'))
        Concavity_Se = int(request.POST.get('concavity_se'))
        Concave_Points_Se = int(request.POST.get('concave_points_se'))
        Symmetry_Se = int(request.POST.get('symmetry_se'))
        Fractal_Dimension_Se = int(request.POST.get('fractal_dimension_se'))
        Radius_Worst = int(request.POST.get('radius_worst'))
        Texture_Worst = int(request.POST.get('texture_worst'))
        Perimeter_Worst = int(request.POST.get('perimeter_worst'))
        Area_Worst = int(request.POST.get('area_worst'))
        Smoothness_Worst = int(request.POST.get('smoothness_worst'))
        Compactness_Worst = int(request.POST.get('compactness_worst'))
        Concavity_Worst = int(request.POST.get('concavity_worst'))
        Concave_Points_Worst = int(request.POST.get('concave_points_worst'))
        Symmetry_Worst = int(request.POST.get('symmetry_worst'))
        Fractal_Dimension_Worst = int(request.POST.get('fractal_dimension_worst'))

        # standardizing variables

        sc = StandardScaler()
        Patient_Age1 = sc.fit_transform([[Patient_Age]])
        Patient_Gender1 = sc.fit_transform([[Patient_Gender]])
        Radius_Mean1 = sc.fit_transform([[Radius_Mean]])
        Texture_Mean1 = sc.fit_transform([[Texture_Mean]])
        Perimeter_Mean1 = sc.fit_transform([[Perimeter_Mean]])
        Area_Mean1 = sc.fit_transform([[Area_Mean]])
        Smoothness_Mean1 = sc.fit_transform([[Smoothness_Mean]])
        Compactness_Mean1 = sc.fit_transform([[Compactness_Mean]])
        Concavity_Mean1 = sc.fit_transform([[Concavity_Mean]])
        Concave_Points_Mean1 = sc.fit_transform([[Concave_Points_Mean]])
        Symmetry_Mean1 = sc.fit_transform([[Symmetry_Mean]])
        Fractal_Dimension_Mean1 = sc.fit_transform([[Fractal_Dimension_Mean]])
        Radius_Se1 = sc.fit_transform([[Radius_Se]])
        Texture_Se1 = sc.fit_transform([[Texture_Se]])
        Perimeter_Se1 = sc.fit_transform([[Perimeter_Se]])
        Area_Se1 = sc.fit_transform([[Area_Se]])
        Smoothness_Se1 = sc.fit_transform([[Smoothness_Se]])
        Compactness_Se1 = sc.fit_transform([[Compactness_Se]])
        Concavity_Se1 = sc.fit_transform([[Concavity_Se]])
        Concave_Points_Se1 = sc.fit_transform([[Concave_Points_Se]])
        Symmetry_Se1 = sc.fit_transform([[Symmetry_Se]])
        Fractal_Dimension_Se1 = sc.fit_transform([[Fractal_Dimension_Se]])
        Radius_Worst1 = sc.fit_transform([[Radius_Worst]])
        Texture_Worst1 = sc.fit_transform([[Texture_Worst]])
        Perimeter_Worst1 = sc.fit_transform([[Perimeter_Worst]])
        Area_Worst1 = sc.fit_transform([[Area_Worst]])
        Smoothness_Worst1 = sc.fit_transform([[Smoothness_Worst]])
        Compactness_Worst1 = sc.fit_transform([[Compactness_Worst]])
        Concavity_Worst1 = sc.fit_transform([[Concavity_Worst]])
        Concave_Points_Worst1 = sc.fit_transform([[Concave_Points_Worst]])
        Symmetry_Worst1 = sc.fit_transform([[Symmetry_Worst]])
        Fractal_Dimension_Worst1 = sc.fit_transform([[Fractal_Dimension_Worst]])

        # Unpickle model
        model = joblib.load("Cancers_model")
        result = model.predict(
            [[ Radius_Mean1[0][0], Texture_Mean1[0][0], Perimeter_Mean1[0][0], Area_Mean1[0][0],
              Smoothness_Mean1[0][0], Compactness_Mean1[0][0], Concavity_Mean1[0][0], Concave_Points_Mean1[0][0], Symmetry_Mean1[0][0], Fractal_Dimension_Mean1[0][0], Radius_Se1[0][0], Texture_Se1[0][0],
              Perimeter_Se1[0][0], Area_Se1[0][0], Smoothness_Se1[0][0], Compactness_Se1[0][0], Concavity_Se1[0][0], Concave_Points_Se1[0][0], Symmetry_Se1[0][0], Fractal_Dimension_Se1[0][0],
              Radius_Worst1[0][0], Texture_Worst1[0][0], Perimeter_Worst1[0][0], Area_Worst1[0][0], Smoothness_Worst1[0][0], Compactness_Worst1[0][0], Concavity_Worst1[0][0], Concave_Points_Worst1[0][0],
              Symmetry_Worst1[0][0], Fractal_Dimension_Worst1[0][0]]])

        Cancer_Disease = result[0]
        '''
        if Heart_Disease == 0:
            disease = "No"
        else:
            disease = "Yes"
        '''

        PredResults.objects.create(Patient_ID=Patient_ID, Patient_Age=Patient_Age, Patient_Gender=Patient_Gender,
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
    data = {"dataset": PredResults.objects.all()}

    return render(request, "doctor_template/results_cancers.html", data)

