from django.db import models

# Create your models here.

class CandidateProfile(models.Model):

    name = models.CharField(max_length=100)
    #bio = models.TextField(max_length=500)
    zip_code = models.CharField(max_length=100)
    skills = models.TextField(max_length=500)
    #github = models.CharField(max_length=50)
    years_experience = models.CharField(max_length=50)
    #education = models.CharField(max_length=50)
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)

class RecruiterProfile(models.Model):

    name = models.CharField(max_length=100)
    company = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=100)
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)

class CreatePost(models.Model):
    
    ## IN SOME WAY ADD AN ID TO BE LATER TO EDIT AND DELETE POSTS IN LATER FEATURES
    position_title = models.CharField(max_length=100)
    type = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    preferred_skills = models.CharField(max_length=100)
    description = models.TextField(max_length=500) 
    company = models.CharField(max_length=100)
    expiration_date = models.DateTimeField('Expiration Date (''DD/MM/YEAR)')
    inactive_date = models.DateTimeField('Inactive Date (''DD/MM/YEAR)')
    is_active = models.BooleanField() # ADD LOGIC TO MAKE THIS INACTIVE ON DATE
