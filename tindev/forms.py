from django.forms import ModelForm
from django import forms
from .models import CandidateProfile
from .models import RecruiterProfile
from .models import CreatePost

class CandidateForm(ModelForm):

    name = forms.TextInput()
    bio = forms.TextInput()
    zip_code = forms.NumberInput()
    skills = forms.TextInput()
    github = forms.TextInput()
    years_experience = forms.NumberInput()
    education = forms.TextInput()
    username = forms.TextInput()
    password = forms.PasswordInput()

    class Meta:
        model = CandidateProfile
        fields = ['name','bio','zip_code','skills','github','years_experience','education','username','password']
        #required = {'name':True,'bio':False,'zip_code':True,'skills':True,'github':False,'years_experience':True,'education':False,'username':True,'password':True}

class RecruiterForm(ModelForm):

    name = forms.TextInput()
    company = forms.TextInput()
    zip_code = forms.TextInput()
    username = forms.TextInput()
    password = forms.PasswordInput()
    
    class Meta:
        model = RecruiterProfile
        fields = ['name', 'company', 'zip_code','username','password']

class CreatePost(ModelForm):
    
    position_title = forms.TextInput()
    type = forms.TextInput()
    location = forms.TextInput()
    preferred_skills = forms.TextInput()
    description = forms.TextInput()
    company = forms.TextInput()
    expiration_date = forms.DateTimeInput()
    inactive_date = forms.DateTimeInput()
    is_active = forms.CheckboxInput()

    class Meta:
        model = CreatePost
        fields = ['position_title','type','location','preferred_skills','description', 'company', 'expiration_date', 'inactive_date', 'is_active']