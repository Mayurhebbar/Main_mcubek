from django.urls import path
from . import views

app_name = "predict_diabetes"

urlpatterns = [
    path('', views.predict_diabetes, name='prediction_page'),
    path('predict_diabetes', views.predict_chances_diabetes, name='submit_prediction'),
    path('result_diabetes', views.view_results_diabetes, name='result'),
]