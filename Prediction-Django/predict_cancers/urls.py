from django.urls import path
from . import views

app_name = "predict_cancers"

urlpatterns = [
    path('', views.predict_cancer, name='prediction_page'),
    path('predict_cancers', views.predict_chances_cancer, name='submit_prediction'),
    path('results_cancers', views.view_results_cancer, name='result'),
]