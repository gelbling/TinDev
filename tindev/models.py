from django.db import models

# this model holds the recruiter profiles and its specific fields
class RecruiterProfile(models.Model):

    name = models.CharField(max_length=100)
    company = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=100)
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)

    def __str__(self):
        return self.name

# this model contains the job posts and its specific fields
class CreatePost(models.Model):

    # used a one to one field to represent the recruiter that created the job post
    recruiter = models.ForeignKey(RecruiterProfile, on_delete=models.CASCADE)
    position_title = models.CharField(max_length=100)
    type = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    preferred_skills = models.CharField(max_length=100)
    description = models.TextField(max_length=500) 
    company = models.CharField(max_length=100)
    expiration_date = models.DateField( )
    is_active = models.BooleanField(default = True, choices=[('False', 'False'), ('True', 'True')]) 

    def __str__(self):
        return self.position_title


# this model holds the candidate profiles and its specific fields
class CandidateProfile(models.Model):

    name = models.CharField(max_length=100)
    bio = models.TextField(max_length=500, blank=True)
    zip_code = models.CharField(max_length=5)
    skills = models.TextField(max_length=500)
    github = models.CharField(max_length=40, blank=True)
    years_experience = models.CharField(max_length=50)
    education = models.CharField(max_length=100, blank=True)
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)

    # used manuy to many fields to represent posts that the user is interested in
    # this field contains objects of the CreatePost model, which are the job posts
    interested = models.ManyToManyField(CreatePost, null=True, blank=True)
    
    def __str__(self):
        return self.name


# this model holds the job offer information and its specific fields
class Offers(models.Model):

    salary = models.CharField(max_length=50)
    due_date = models.DateField( )
    acepted = models.BooleanField(null=True, blank=True, choices=[('False', 'False'), ('True', 'True')])
    
    # used one to one key to represent the candidate that has the job offer
    candidate = models.ForeignKey(CandidateProfile, on_delete=models.CASCADE, null=True, blank=True)
    # used one to one key to represent the job post correlated to this offer
    job = models.ForeignKey(CreatePost, on_delete=models.CASCADE, null=True, blank=True)