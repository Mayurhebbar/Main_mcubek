from django.db import models


class PredResults_heart(models.Model):

    Patient_ID = models.IntegerField()
    Patient_Age = models.IntegerField()
    Patient_Gender = models.IntegerField()
    Patient_Name = models.CharField(max_length=255)
    consulted_doctor = models.IntegerField()
    CP = models.IntegerField()
    Trestbps = models.IntegerField()
    Cholesterol = models.IntegerField()
    FBS = models.FloatField()
    Restecg = models.IntegerField()
    Thalach = models.IntegerField()
    Exang = models.IntegerField()
    Oldpeak = models.FloatField()
    Slope = models.IntegerField()
    CA = models.FloatField()
    Thal = models.IntegerField()
    Heart_Disease = models.CharField(max_length=30)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.Heart_Disease
