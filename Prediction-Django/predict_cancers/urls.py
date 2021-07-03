from django.urls import path
from . import views

app_name = "predict_cancers"

urlpatterns = [
    path('', views.predict_cancers, name='prediction_page'),
    path('predict_cancers', views.predict_chances_cancers, name='submit_prediction'),
    path('results_cancers', views.view_results_cancers, name='result'),
    #path('pdf_view/', views.render_pdf_view, name='pdf-view'),
    path('pdf/<int:Patient_ID>/', views.predict_cancers_render_pdf_view, name='predict_cancers-pdf-view'),
]