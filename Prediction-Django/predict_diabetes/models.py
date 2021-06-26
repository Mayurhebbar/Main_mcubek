from django.db import models


class PredResults_diabetes(models.Model):

    Patient_ID = models.IntegerField()
    Patient_Age = models.IntegerField()
    Patient_Gender = models.IntegerField()
    Diabetes_Disease = models.CharField(max_length=30)

    def __str__(self):
        return self.Diabetes_Disease