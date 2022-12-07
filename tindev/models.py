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
    position_title = models.CharField(max_length=100)
    type = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    preferred_skills = models.CharField(max_length=100)
    description = models.TextField(max_length=500) 
    company = models.CharField(max_length=100)
    expiration_date = models.DateField( )
    is_active = models.BooleanField(default = True, choices=[('False', 'False'), ('True', 'True')]) # ADD LOGIC TO MAKE THIS INACTIVE ON DATE

    def __str__(self):
        return self.position_title

class CandidateProfile(models.Model):

    name = models.CharField(max_length=100)
    bio = models.TextField(max_length=500, blank=True)
    zip_code = models.CharField(max_length=100)
    skills = models.TextField(max_length=500)
    github = models.CharField(max_length=40, blank=True)
    years_experience = models.CharField(max_length=50)
    education = models.CharField(max_length=100, blank=True)
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)

    interested = models.ManyToManyField(CreatePost, null=True, blank=True)

    def __str__(self):
        return self.name

