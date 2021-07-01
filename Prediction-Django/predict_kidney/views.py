import joblib
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
import pandas as pd
from django.http import HttpResponse
from .models import PredResults_kidney
from home.models import CustomUser, Doctors
from sklearn.preprocessing import StandardScaler
from django.template.loader import get_template
from xhtml2pdf import pisa


def predict_kidney_render_pdf_view(request, *args, **kwargs):
    Patient_ID = kwargs.get('Patient_ID')
    predict_kidney = get_object_or_404(PredResults_kidney, Patient_ID=Patient_ID)
    doctor_details = get_object_or_404(CustomUser, id=request.user.id)
    doctor_details_new = get_object_or_404(Doctors, admin_id=request.user.id)
    template_path = 'predict_kidney/pdf2.html'
    context = {'predict_kidney': predict_kidney, 'doctor_details': doctor_details, 'doctor_details_new': doctor_details_new}
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
        Patient_Name = str(request.POST.get('Patient_Name'))
        Patient_ID = float(request.POST.get('Patient_ID'))
        Patient_Gender = float(request.POST.get('Patient_Gender'))
        Patient_Age = float(request.POST.get('Patient_Age'))
        BP = float(request.POST.get('bp'))
        AL = float(request.POST.get('al'))
        PCV = float(request.POST.get('pcv'))
        PCC = float(request.POST.get('pcc'))
        BGR = float(request.POST.get('bgr'))
        BU = float(request.POST.get('bu'))
        SC = float(request.POST.get('sc'))
        HEMO = float(request.POST.get('hemo'))
        HTN = float(request.POST.get('htn'))
        DM = float(request.POST.get('dm'))
        APPET = float(request.POST.get('appet'))
        #The below fields are not necessary for prediction
        SG = float(request.POST.get('sg'))
        SU = float(request.POST.get('su'))
        RBC = float(request.POST.get('rbc'))
        PC = float(request.POST.get('pc'))
        BA = float(request.POST.get('ba'))
        SOD = float(request.POST.get('sod'))
        POT = float(request.POST.get('pot'))
        WC = float(request.POST.get('wc'))
        RC = float(request.POST.get('rc'))
        CAD = float(request.POST.get('cada'))
        PE = float(request.POST.get('pe'))
        ANE = float(request.POST.get('ane'))
        consulted_doctor = request.user.id

        # Unpickle model
        #De serialize the model and predict

        model = joblib.load("kidney_model")
        result = model.predict([[Patient_Age, BP, AL, PCC, BGR, BU,
                                 SC, HEMO, PCV, HTN, DM, APPET]])

        Kidney_Disease = result[0]

        if Kidney_Disease == 0:
            disease = "No Risk of Chronic Kidney Disease"
        else:
            disease = "At Risk of Chronic Kidney Disease"

        patients_lists = PredResults_kidney.objects.all()
        ID_list = []
        for patients_list in patients_lists:
            individual_list = patients_list.Patient_ID
            ID_list.append(individual_list)

        if Patient_ID not in ID_list:
            user = PredResults_kidney(Patient_ID=Patient_ID, Patient_Name=Patient_Name, Patient_Age=Patient_Age,
                               Patient_Gender=Patient_Gender,
                               Kidney_Disease=Kidney_Disease, BP=BP, AL=AL, PCV=PCV,
                               PCC=PCC, BGR=BGR,
                               BU=BU, SC=SC, HEMO=HEMO, HTN=HTN, DM=DM,
                               APPET=APPET, SG=SG, SU=SU, RBC=RBC, PC=PC, BA=BA, SOD=SOD, POT=POT, WC=WC, RC=RC, CAD=CAD,
                               PE=PE, ANE=ANE, consulted_doctor=consulted_doctor)
            user.save()
        else:
            update_list = PredResults_kidney.objects.get(Patient_ID=Patient_ID)
            update_list.Patient_Age = Patient_Age
            update_list.Patient_Name = Patient_Name
            update_list.Kidney_Disease = Kidney_Disease
            update_list.BP = BP
            update_list.AL = AL
            update_list.PCV = PCV
            update_list.PCC = PCC
            update_list.BGR = BGR
            update_list.BU = BU
            update_list.SC = SC
            update_list.HEMO = HEMO
            update_list.HTN = HTN
            update_list.DM = DM
            update_list.APPET = APPET
            update_list.SG = SG
            update_list.SU = SU
            update_list.RBC = RBC
            update_list.PC = PC
            update_list.BA = BA
            update_list.SOD = SOD
            update_list.POT = POT
            update_list.WC = WC
            update_list.RC = RC
            update_list.CAD = CAD
            update_list.PE = PE
            update_list.ANE = ANE
            update_list.consulted_doctor = consulted_doctor
            update_list.save()


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


        return JsonResponse({'result': disease, 'Patient_ID': Patient_ID, 'Patient_Name':Patient_Name, 'Patient_Age': Patient_Age,
                             'Patient_Gender': Patient_Gender, 'bp': BP, 'al': AL,
                             'pcc': PCC, 'bgr': BGR, 'bu': BU, 'sc': SC, 'hemo': HEMO, 'pcv': PCV, 'htn': HTN, 'dm': DM,
                             'appet': APPET,'sg':SG, 'su':SU, 'rbc':RBC, 'pc':PC, 'ba':BA, 'sod':SOD, 'pot':POT, 'wc':WC,
                             'rc':RC, 'cada':CAD, 'pe':PE, 'ane':ANE},
                            safe=False)


def view_results_kidney(request):
    # Submit prediction and show all
    data = {"dataset": PredResults_kidney.objects.all()}
    return render(request, "doctor_template/results_kidney.html", data)
