from django.db import models

# Create your models here.

class CandidateProfile(models.Model):

    name = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=100)
    skills = models.CharField(max_length=500)
    years_experience = models.CharField(max_length=50)
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)