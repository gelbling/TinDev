from django.forms import ModelForm
from django import forms
from .models import CandidateProfile

class CandidateForm(ModelForm):

    name = forms.TextInput()
    zip_code = forms.TextInput()
    skills = forms.TextInput()
    years_experience = forms.TextInput()
    username = forms.TextInput()
    password = forms.TextInput()

    class Meta:
        model = CandidateProfile
        fields = ['name', 'zip_code','skills','years_experience','username','password']