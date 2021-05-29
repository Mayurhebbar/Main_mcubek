from django.urls import path
from . import views

app_name = "predict_kidney"

urlpatterns = [
    path('', views.predict_kidney, name='prediction_page'),
    path('predict_kidney', views.predict_chances_kidney, name='submit_prediction'),
    path('results_kidney', views.view_results_kidney, name='result'),
]