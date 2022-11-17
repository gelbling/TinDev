from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from tindev.forms import CandidateForm
from tindev.models import CandidateProfile
from tindev.forms import RecruiterForm
from tindev.models import RecruiterProfile
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm


def login(request):
    
    return render(request, 'tindev/login.html')

def candidateProfile(request):
    if request.POST:
        form = CandidateForm(request.POST)
        if form.is_valid():
            form.save()
        return redirect(login)
    return render(request, 'tindev/candidateProfile.html', {'form':CandidateForm}) 

def recruiterProfile(request):
    if request.POST:
        form = RecruiterForm(request.POST)
        if form.is_valid():
            form.save()
        return redirect(login)
    return render(request, 'tindev/recruiterProfile.html', {'form':RecruiterForm}) 

def home(request):
    
    return render(request, 'tindev/home.html') 
	