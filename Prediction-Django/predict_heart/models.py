from django.db import models


class PredResults(models.Model):

    Patient_ID = models.IntegerField()
    Patient_Age = models.IntegerField()
    Patient_Gender = models.IntegerField()
    Patient_Name = models.CharField(max_length=255)
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

    def __str__(self):
        return self.Heart_Disease
