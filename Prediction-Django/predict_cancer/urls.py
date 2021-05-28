from django.urls import path
from . import views

app_name = "predict_heart"

urlpatterns = [
    path('', views.predict_heart, name='prediction_page'),
    path('predict_heart', views.predict_chances_heart, name='submit_prediction'),
    path('results_heart', views.view_results_heart, name='result'),
]