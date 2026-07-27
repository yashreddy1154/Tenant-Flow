from django.db import models

# Create your models here.
class User(models.Model):
    email = models.EmailField(primary_key=True)
    password= models.CharField(max_length=100)
    