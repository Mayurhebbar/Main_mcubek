import joblib
from django.shortcuts import render
from django.http import JsonResponse
import pandas as pd
from .models import PredResults
from sklearn.preprocessing import StandardScaler


def predict_kidney(request):
    return render(request, 'doctor_template/predict_kidney.html')


def predict_chances_kidney(request):
    if request.POST.get('action') == 'post':
        # Receive data from client
        Patient_ID = int(request.POST.get('Patient_ID'))
        Patient_Gender = int(request.POST.get('Patient_Gender'))
        Patient_Age = int(request.POST.get('Patient_Age'))
        BP = int(request.POST.get('bp'))
        AL = int(request.POST.get('al'))
        PCV = int(request.POST.get('pcv'))
        PCC = int(request.POST.get('pcc'))
        BGR = int(request.POST.get('bgr'))
        BU = int(request.POST.get('bu'))
        SC = float(request.POST.get('sc'))
        HEMO = float(request.POST.get('hemo'))
        HTN = int(request.POST.get('htn'))
        DM = int(request.POST.get('dm'))
        APPET = int(request.POST.get('appet'))

        '''
        The below fields are not necessary for prediction
        
        SG = float(request.POST.get('sg'))
        SU = int(request.POST.get('su'))
        RBC = int(request.POST.get('rbc'))
        PC = int(request.POST.get('pc'))
        BA = int(request.POST.get('ba'))
        SOD = int(request.POST.get('sod'))
        POT = float(request.POST.get('pot'))
        WC = int(request.POST.get('wc'))
        RC = float(request.POST.get('rc'))
        CAD = int(request.POST.get('cad'))
        PE = int(request.POST.get('pe'))
        ANE = int(request.POST.get('ane'))
        '''

        # standardizing variables

        sc = StandardScaler()
        Patient_Age1 = sc.fit_transform([[Patient_Age]])
        BP1 = sc.fit_transform([[BP]])
        PCV1 = sc.fit_transform([[PCV]])
        AL1 = sc.fit_transform([[AL]])
        PCC1 = sc.fit_transform([[PCC]])
        BGR1 = sc.fit_transform([[BGR]])
        BU1 = sc.fit_transform([[BU]])
        SC1 = sc.fit_transform([[SC]])
        HEMO1 = sc.fit_transform([[HEMO]])
        HTN1 = sc.fit_transform([[HTN]])
        DM1 = sc.fit_transform([[DM]])
        APPET1 = sc.fit_transform([[APPET]])


        # Unpickle model

        model = joblib.load("kidney_model")
        result = model.predict([[Patient_Age1[0][0], BP1[0][0], AL1[0][0], PCC1[0][0], BGR1[0][0], BU1[0][0],
                                 SC1[0][0], HEMO1[0][0], PCV1[0][0], HTN1[0][0], DM1[0][0], APPET1[0][0]]])

        Kidney_Disease = result[0]
        '''
        if Kidney_Disease == 0:
            disease = "No"
        else:
            disease = "Yes"
        '''

        PredResults.objects.create(Patient_ID=Patient_ID, Patient_Age=Patient_Age, Patient_Gender=Patient_Gender,
                                   Kidney_Disease=int(Kidney_Disease))
        '''
        if Patient_Gender == 0:
            gender = "Female"
        else:
            gender = "Male"

        if PCC == 0:
            pcc = "Not Present"
        else:
            pcc = "Present"

        if HTN == 0:
            htn = "No"
        else:
            htn = "Yes"

        if DM == 0:
            dm = "No"
        else:
            dm = "Yes"

        if APPET == 0:
            appet = "Poor"
        else:
            appet = "Good"
        '''

        return JsonResponse({'result': Kidney_Disease, 'Patient_ID': Patient_ID, 'Patient_Age': Patient_Age,
                             'Patient_Gender': Patient_Gender, 'bp': BP, 'al': AL,
                             'pcc': PCC, 'bgr': BGR, 'bu': BU, 'sc': SC, 'hemo': HEMO, 'pcv': PCV, 'htn': HTN, 'dm': DM,
                             'appet': APPET},
                            safe=False)


def view_results_kidney(request):
    # Submit prediction and show all
    data = {"dataset": PredResults.objects.all()}
    return render(request, "doctor_template/results_kidney.html", data)
