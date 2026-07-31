from django.db import models

# Create your models here.

class Organization(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=500, blank=True)
    industry_type = models.CharField(max_length=100, blank=True)
    company_size = models.IntegerField(null=True, blank=True)
    logo = models.ImageField(upload_to='org_logos/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name