import joblib
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
import pandas as pd
from .models import PredResults
from sklearn.preprocessing import StandardScaler
import numpy as np
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa


def predict_heart_render_pdf_view(request, *args, **kwargs):
    Patient_ID = kwargs.get('Patient_ID')
    predict_heart = get_object_or_404(PredResults, Patient_ID=Patient_ID)
    template_path = 'predict_heart/pdf2.html'
    context = {'predict_heart': predict_heart}
    # Create a Django response object, and specify content_type as pdf
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="Heart Disease Report.pdf"'
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


'''
def render_pdf_view(request):
    template_path = 'predict_heart/pdf1.html'
    context = {'myvar': 'this is your template context'}
    # Create a Django response object, and specify content_type as pdf
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="Report.pdf"'
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
'''


def predict_heart(request):
    return render(request, 'doctor_template/predict_heart.html')


def predict_chances_heart(request):
    if request.POST.get('action') == 'post':
        # Receive data from client
        Patient_Name = str(request.POST.get('Patient_Name'))
        Patient_ID = float(request.POST.get('Patient_ID'))
        Patient_Age = str(request.POST.get('Patient_Age'))
        Patient_Gender = float(request.POST.get('Patient_Gender'))
        CP = float(request.POST.get('cp'))
        Trestbps = float(request.POST.get('trestbps'))
        Cholesterol = float(request.POST.get('chol'))
        FBS = float(request.POST.get('fbs'))
        Restecg = float(request.POST.get('restecg'))
        Thalach = float(request.POST.get('thalach'))
        Exang = float(request.POST.get('exang'))
        Oldpeak = float(request.POST.get('oldpeak'))
        Slope = float(request.POST.get('slope'))
        CA = float(request.POST.get('ca'))
        Thal = float(request.POST.get('thal'))

        # standardizing variables
        sc_test = joblib.load("Heart_Standard_Scalar")
        model_test = joblib.load("heart_model")

        # Array Input Ndarray
        array_input = [
            [Patient_Age, Patient_Gender, CP, Trestbps, Cholesterol, Restecg, Thalach, Exang, Oldpeak, Slope, Thal]]

        # Logging the index variables in the dataframe
        array_input[0][3] = np.log(array_input[0][3])
        array_input[0][4] = np.log(array_input[0][4])

        # Transform the model using the Standard Scalar desreialised object
        array_input = sc_test.transform(array_input)

        # Predict the output using heart_model ML deserialize object
        result = model_test.predict(array_input)

        # Results obtained from the deserialized object(ML object)
        Heart_Disease = result[0]

        if Heart_Disease == 0:
            disease = "No Risk"
        else:
            disease = "At Risk"

        # PredResults.objects.create(Patient_ID=Patient_ID, Patient_Age=Patient_Age, Patient_Gender=Patient_Gender,
        #                          Heart_Disease=Heart_Disease)
        patients_lists = PredResults.objects.all()
        ID_list = []
        for patients_list in patients_lists:
            individual_list = patients_list.Patient_ID
            ID_list.append(individual_list)

        if Patient_ID not in ID_list:
            user = PredResults(Patient_ID=Patient_ID, Patient_Name=Patient_Name, Patient_Age=Patient_Age,
                               Patient_Gender=Patient_Gender,
                               Heart_Disease=Heart_Disease, CP=CP, Trestbps=Trestbps, FBS=FBS,
                               Cholesterol=Cholesterol, Restecg=Restecg,
                               Thalach=Thalach, Exang=Exang, Oldpeak=Oldpeak, Slope=Slope, CA=CA,
                               Thal=Thal)
            user.save()
        else:
            update_list = PredResults.objects.get(Patient_ID=Patient_ID)
            update_list.Patient_Age = Patient_Age
            update_list.Heart_Disease = Heart_Disease
            update_list.CP = CP
            update_list.Trestbps = Trestbps
            update_list.FBS = FBS
            update_list.Cholesterol = Cholesterol
            update_list.Restecg = Restecg
            update_list.Thalach = Thalach
            update_list.Exang = Exang
            update_list.Oldpeak = Oldpeak
            update_list.Slope = Slope
            update_list.CA = CA
            update_list.Thal = Thal
            update_list.save()

        if Patient_Gender == 0:
            gender = "Female"
        else:
            gender = "Male"

        if Exang == 0:
            exang_value = "No"
        else:
            exang_value = "Yes"

        if FBS == 0:
            fasting = "False"
        else:
            fasting = "True"

        if Restecg == 0:
            rest = "Normal"
        elif Restecg == 1:
            rest = "Having ST - T Wave Abnormality"
        else:
            rest = "Hypertrophy"

        if Thal == 0:
            thal_value = "Normal"
        elif Thal == 1:
            thal_value = "Fixed Defect"
        else:
            thal_value = "Reversable Defect"

        if CP == 0:
            Chest_Pain = "Typical Angina"
        elif CP == 1:
            Chest_Pain = "Atypical Angina"
        elif CP == 2:
            Chest_Pain = "Non - Anginal Pain"
        else:
            Chest_Pain = "Asymptomatic"

        if Slope == 0:
            slope_value = "Upsloping"
        elif Slope == 1:
            slope_value = "Flat"
        else:
            slope_value = "Downsloping"

        return JsonResponse(
            {'result': disease, 'Patient_ID': Patient_ID, 'Patient_Name': Patient_Name, 'Patient_Age': Patient_Age,
             'Patient_Gender': gender, 'cp': Chest_Pain, 'trestbps': Trestbps, 'chol': Cholesterol,
             'restecg': rest, 'thalach': Thalach, 'exang': exang_value, 'oldpeak': Oldpeak, 'slope': slope_value,
             'thal': thal_value, 'fbs': fasting, 'ca': CA},
            safe=False)


def view_results_heart(request):
    # Submit prediction and show all
    data = {"dataset": PredResults.objects.all()}
    return render(request, "doctor_template/results_heart.html", data)
