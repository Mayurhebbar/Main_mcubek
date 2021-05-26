from django.db import models


class PredResults(models.Model):

    Patient_ID = models.IntegerField()
    Patient_Age = models.IntegerField()
    Patient_Gender = models.IntegerField()
    Cancer_Disease = models.CharField(max_length=30)

    def __str__(self):
        return self.Cancer_Disease