from django.db import models

# Create your models here.

class RecruiterProfile(models.Model):

    name = models.CharField(max_length=100)
    company = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=100)
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class CreatePost(models.Model):

    recruiter = models.ForeignKey(RecruiterProfile, on_delete=models.CASCADE)
    ## IN SOME WAY ADD AN ID TO BE LATER TO EDIT AND DELETE POSTS IN LATER FEATURES
    position_title = models.CharField(max_length=100)
    type = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    preferred_skills = models.CharField(max_length=100)
    description = models.TextField(max_length=500) 
    company = models.CharField(max_length=100)
    #expiration_date = models.DateField('Expiration Date (''YEAR/MM/DD)')
    #inactive_date = models.DateField('Inactive Date (''YEAR/MM/DD)')
    expiration_date = models.CharField(max_length=100)
    inactive_date = models.CharField(max_length=100)
    is_active = models.BooleanField() # ADD LOGIC TO MAKE THIS INACTIVE ON DATE

    def __str__(self):
        return self.position_title

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

    interested = models.ManyToManyField(CreatePost, null=True, blank=True)

    def __str__(self):
        return self.name

