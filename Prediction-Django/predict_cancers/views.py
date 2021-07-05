import joblib
from django.shortcuts import render,  get_object_or_404
from django.http import JsonResponse
import pandas as pd
from .models import PredResults_cancers
from home.models import CustomUser, Doctors
from sklearn.preprocessing import StandardScaler
import numpy as np
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa


def predict_cancers_render_pdf_view(request, *args, **kwargs):
    Patient_ID = kwargs.get('Patient_ID')
    predict_cancers = get_object_or_404(PredResults_cancers, Patient_ID=Patient_ID)
    doctor_details = get_object_or_404(CustomUser, id=request.user.id)
    doctor_details_new = get_object_or_404(Doctors, admin_id=request.user.id)
    template_path = 'predict_cancers/pdf2.html'
    context = {'predict_cancers': predict_cancers, 'doctor_details': doctor_details, 'doctor_details_new': doctor_details_new}
    # Create a Django response object, and specify content_type as pdf
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="Cancer Disease Report.pdf"'
    # find the template and render it.
    template = get_template(template_path)
    html = template.render(context)

    # create a pdf
    pisa_status = pisa.CreatePDF(
        html, dest=response)
    # if error then show some funy view
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response


def predict_cancers(request):
    return render(request, 'doctor_template/predict_cancers.html')


def predict_chances_cancers(request):
    if request.POST.get('action') == 'post':
        # Receive data from client
        Patient_Name = str(request.POST.get('Patient_Name'))
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
        consulted_doctor = request.user.id

        #Deserailize the joblib object and READY TO PREDICT THE RESULT
        # Unpickle model
        model = joblib.load("Cancers_model")
        
        result = model.predict(
            [[Radius_Mean, Texture_Mean, Perimeter_Mean, Area_Mean,
              Smoothness_Mean, Compactness_Mean, Concavity_Mean, Concave_Points_Mean, Symmetry_Mean, Fractal_Dimension_Mean, Radius_Se, Texture_Se,
              Perimeter_Se, Area_Se, Smoothness_Se, Compactness_Se, Concavity_Se, Concave_Points_Se, Symmetry_Se, Fractal_Dimension_Se,
              Radius_Worst, Texture_Worst, Perimeter_Worst, Area_Worst, Smoothness_Worst, Compactness_Worst, Concavity_Worst, Concave_Points_Worst,
              Symmetry_Worst, Fractal_Dimension_Worst]])

        probability = model.predict_proba([[Radius_Mean, Texture_Mean, Perimeter_Mean, Area_Mean,
              Smoothness_Mean, Compactness_Mean, Concavity_Mean, Concave_Points_Mean, Symmetry_Mean, Fractal_Dimension_Mean, Radius_Se, Texture_Se,
              Perimeter_Se, Area_Se, Smoothness_Se, Compactness_Se, Concavity_Se, Concave_Points_Se, Symmetry_Se, Fractal_Dimension_Se,
              Radius_Worst, Texture_Worst, Perimeter_Worst, Area_Worst, Smoothness_Worst, Compactness_Worst, Concavity_Worst, Concave_Points_Worst,
              Symmetry_Worst, Fractal_Dimension_Worst]])

        probab_perc=round(probability[0][1]*100,3)

        print(probab_perc)

        Cancer_Disease = result[0]
        print(Cancer_Disease)

        if Cancer_Disease == 0:
            disease = "Benign (Indicates Absence of Cancer Cells) i.e Patient might not be At Risk"
        else:
            disease = "Malignant (Indicates Presence of Cancer Cells) i.e Patient might be At Risk"

        patients_lists = PredResults_cancers.objects.all()
        ID_list = []
        for patients_list in patients_lists:
            individual_list = patients_list.Patient_ID
            ID_list.append(individual_list)

        if Patient_ID not in ID_list:
            user = PredResults_cancers(Patient_ID=Patient_ID, Patient_Name=Patient_Name, Patient_Age=Patient_Age,
                                     Patient_Gender=Patient_Gender,
                                     Cancer_Disease=Cancer_Disease, Radius_Mean=Radius_Mean, Texture_Mean=Texture_Mean, Perimeter_Mean=Perimeter_Mean,
                                     Area_Mean=Area_Mean, Smoothness_Mean=Smoothness_Mean,Compactness_Mean=Compactness_Mean, Concavity_Mean=Concavity_Mean, Concave_Points_Mean=Concave_Points_Mean, Symmetry_Mean=Symmetry_Mean, Fractal_Dimension_Mean=Fractal_Dimension_Mean,
                                     Radius_Se=Radius_Se, Texture_Se=Texture_Se, Perimeter_Se=Perimeter_Se,
                                     Area_Se=Area_Se, Smoothness_Se=Smoothness_Se,Compactness_Se=Compactness_Se, Concavity_Se=Concavity_Se, Concave_Points_Se=Concave_Points_Se, Symmetry_Se=Symmetry_Se, Fractal_Dimension_Se=Fractal_Dimension_Se,
                                     Radius_Worst=Radius_Worst,
                                     Texture_Worst=Texture_Worst, Perimeter_Worst=Perimeter_Worst,
                                     Area_Worst=Area_Worst, Smoothness_Worst=Smoothness_Worst,
                                     Compactness_Worst=Compactness_Worst, Concavity_Worst=Concavity_Worst,
                                     Concave_Points_Worst=Concave_Points_Worst, Symmetry_Worst=Symmetry_Worst,
                                     Fractal_Dimension_Worst=Fractal_Dimension_Worst, consulted_doctor=consulted_doctor,probability_percentage_cancer=probab_perc)
            user.save()
        else:
            update_list = PredResults_cancers.objects.get(Patient_ID=Patient_ID)
            update_list.Patient_Age = Patient_Age
            update_list.Cancer_Disease = Cancer_Disease
            update_list.Radius_Mean = Radius_Mean
            update_list.Texture_Mean = Texture_Mean
            update_list.Perimeter_Mean = Perimeter_Mean
            update_list.Area_Mean = Area_Mean
            update_list.Smoothness_Mean = Smoothness_Mean
            update_list.Compactness_Mean = Compactness_Mean
            update_list.Concavity_Mean = Concavity_Mean
            update_list.Concave_Points_Mean = Concave_Points_Mean
            update_list.Symmetry_Mean = Symmetry_Mean
            update_list.Fractal_Dimension_Mean = Fractal_Dimension_Mean
            update_list.Radius_Se = Radius_Se
            update_list.Texture_Se = Texture_Se
            update_list.Perimeter_Se = Perimeter_Se
            update_list.Area_Se = Area_Se
            update_list.Smoothness_Se = Smoothness_Se
            update_list.Compactness_Se = Compactness_Se
            update_list.Concavity_Se = Concavity_Se
            update_list.Concave_Points_Se = Concave_Points_Se
            update_list.Symmetry_Se = Symmetry_Se
            update_list.Fractal_Dimension_Se = Fractal_Dimension_Se
            update_list.Radius_Worst = Radius_Worst
            update_list.Texture_Worst = Texture_Worst
            update_list.Perimeter_Worst = Perimeter_Worst
            update_list.Area_Worst = Area_Worst
            update_list.Smoothness_Worst = Smoothness_Worst
            update_list.Compactness_Worst = Compactness_Worst
            update_list.Concavity_Worst = Concavity_Worst
            update_list.Concave_Points_Worst = Concave_Points_Worst
            update_list.Symmetry_Worst = Symmetry_Worst
            update_list.Fractal_Dimension_Worst = Fractal_Dimension_Worst
            update_list.consulted_doctor = consulted_doctor
            update_list.probability_percentage_cancer = probab_perc
            update_list.save()

        if Patient_Gender == 0:
            gender = "Female"
        else:
            gender = "Male"



        return JsonResponse({'result': disease, 'prediction_percentage': probab_perc, 'Patient_ID': Patient_ID, 'Patient_Name': Patient_Name, 'Patient_Age': Patient_Age,
                             'Patient_Gender': gender, 'radius_mean': Radius_Mean, 'texture_mean': Texture_Mean, 'perimeter_mean': Perimeter_Mean,
                             'area_mean': Area_Mean, 'smoothness_mean': Smoothness_Mean, 'compactness_mean': Compactness_Mean, 'concavity_mean': Concavity_Mean,'concave_points_mean': Concave_Points_Mean, 'symmetry_mean': Symmetry_Mean,
                             'fractal_dimension_mean': Fractal_Dimension_Mean, 'radius_se': Radius_Se, 'texture_se': Texture_Se, 'perimeter_se': Perimeter_Se,
                             'area_se': Area_Se, 'smoothness_se': Smoothness_Se, 'compactness_se': Compactness_Se, 'concavity_se': Concavity_Se,
                             'concave_points_se': Concave_Points_Se, 'symmetry_se': Symmetry_Se, 'fractal_dimension_se': Fractal_Dimension_Se, 'radius_worst': Radius_Worst,
                             'texture_worst': Texture_Worst, 'perimeter_worst': Perimeter_Worst, 'area_worst': Area_Worst, 'smoothness_worst': Smoothness_Worst,
                             'compactness_worst': Compactness_Worst, 'concavity_worst': Concavity_Worst, 'concave_points_worst': Concave_Points_Worst, 'symmetry_worst': Symmetry_Worst,
                             'fractal_dimension_worst': Fractal_Dimension_Worst},
                            safe=False)


def view_results_cancers(request):
    # Submit prediction and show all
    data = {"dataset": PredResults_cancers.objects.all()}

    return render(request, "doctor_template/results_cancers.html", data)

