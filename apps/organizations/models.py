from django.db import models

# Create your models here.

class Organizations(models.Model):
    Organization_Name = models.CharField(max_length=100)
    Description = models.CharField(max_length=500)
    Industry_Type = models.CharField(max_length=100)
    Industry_Size = models.IntegerField()    