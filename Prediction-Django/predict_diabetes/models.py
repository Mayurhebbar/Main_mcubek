from django.db import models


class PredResults_diabetes(models.Model):

    Patient_ID = models.IntegerField()
    Patient_Age = models.IntegerField()
    Patient_Name = models.CharField(max_length=255)
    Patient_Gender = models.IntegerField()
    consulted_doctor = models.IntegerField()
    Pregnancies=models.IntegerField()
    Glucose=models.IntegerField()
    BloodPressure=models.IntegerField()
    SkinThickness=models.IntegerField()
    Insulin=models.IntegerField()
    BMI=models.FloatField()
    DiabetesPedigreeFunction=models.FloatField()
    Diabetes_Disease = models.CharField(max_length=30)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.Diabetes_Disease