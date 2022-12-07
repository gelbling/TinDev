from django.forms import ModelForm
from django import forms
from .models import CandidateProfile
from .models import RecruiterProfile
from .models import CreatePost
from django.shortcuts import render
from crispy_forms.helper import FormHelper
from django.forms.widgets import DateInput

class CandidateForm(ModelForm):

    name = forms.TextInput()
    bio = forms.TextInput(attrs = {'required': False})
    zip_code = forms.NumberInput()
    skills = forms.TextInput()
    github = forms.TextInput(attrs = {'required': False})
    years_experience = forms.NumberInput()
    education = forms.TextInput(attrs = {'required': False})
    username = forms.TextInput()
    password = forms.PasswordInput()

    class Meta:
        model = CandidateProfile
        fields = ['name', 'bio', 'zip_code', 'skills', 'github', 'years_experience', 'education', 'username', 'password']

class RecruiterForm(ModelForm):

    name = forms.TextInput()
    company = forms.TextInput()
    zip_code = forms.TextInput()
    username = forms.TextInput()
    password = forms.PasswordInput()
    
    class Meta:
        model = RecruiterProfile
        fields = ['name', 'company', 'zip_code','username','password']

class CreatePostForm(ModelForm):
    
    position_title = forms.TextInput()
    type = forms.TextInput()
    location = forms.TextInput()
    preferred_skills = forms.TextInput()
    description = forms.TextInput()
    company = forms.TextInput()
    expiration_date = forms.DateField(widget=forms.widgets.DateInput(attrs={'type': 'date'}))
#   is_active = forms.CheckboxInput()

    class Meta:
        model = CreatePost
        fields = ['position_title','type','location','preferred_skills','description', 'company', 'expiration_date']