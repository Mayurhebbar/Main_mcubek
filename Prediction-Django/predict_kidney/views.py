import joblib
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
import pandas as pd
from django.http import HttpResponse
from .models import PredResults_kidney
from sklearn.preprocessing import StandardScaler
from django.template.loader import get_template
from xhtml2pdf import pisa


def predict_kidney_render_pdf_view(request, *args, **kwargs):
    Patient_ID = kwargs.get('Patient_ID')
    predict_kidney = get_object_or_404(PredResults_kidney, Patient_ID=Patient_ID)
    template_path = 'predict_kidney/pdf2.html'
    context = {'predict_kidney': predict_kidney}
    # Create a Django response object, and specify content_type as pdf
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="Kidney Disease Report.pdf"'
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


def predict_kidney(request):
    return render(request, 'doctor_template/predict_kidney.html')


def predict_chances_kidney(request):
    if request.POST.get('action') == 'post':
        # Receive data from client
        #Patient_Name = str(request.POST.get('Patient_Name'))
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
        SU = float(request.POST.get('su'))
        RBC = float(request.POST.get('rbc'))
        PC = float(request.POST.get('pc'))
        BA = float(request.POST.get('ba'))
        SOD = float(request.POST.get('sod'))
        POT = float(request.POST.get('pot'))
        WC = float(request.POST.get('wc'))
        RC = float(request.POST.get('rc'))
        CAD = float(request.POST.get('cad'))
        PE = float(request.POST.get('pe'))
        ANE = float(request.POST.get('ane'))
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

        PredResults_kidney.objects.create(Patient_ID=Patient_ID, Patient_Age=Patient_Age, Patient_Gender=Patient_Gender,
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
    data = {"dataset": PredResults_kidney.objects.all()}
    return render(request, "doctor_template/results_kidney.html", data)
