from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from tindev.forms import CandidateForm
from tindev.models import CandidateProfile
from tindev.forms import RecruiterForm
from tindev.models import RecruiterProfile
from tindev.forms import CreatePost
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User



def user_login(request):

    if request.POST:

        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is None:
            context = {'error':'Invalid username or password'}
            return render(request, 'tindev/login.html', context)

        login(request,user)
        return render(request, 'tindev/loggedin.html')

    return render(request, 'tindev/login.html')



def candidateProfile(request):
    if request.POST:
        form = CandidateForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(username=form.cleaned_data['username'],
                                 password=form.cleaned_data['password'])
            form.save()
        return redirect(user_login)
    return render(request, 'tindev/candidateProfile.html', {'form':CandidateForm}) 



def recruiterProfile(request):
    if request.POST:
        form = RecruiterForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(username=form.cleaned_data['username'],
                                 password=form.cleaned_data['password'])
            form.save()
        return redirect(user_login)
    return render(request, 'tindev/recruiterProfile.html', {'form':RecruiterForm}) 



def home(request):

    return render(request, 'tindev/home.html')

def candidateDashboard(request):

    return render(request, 'tindev/candidateDashboard.html')

def recruiterDashboard(request):

    return render(request, 'tindev/recruiterDashboard.html')

def createPost(request):
    if request.POST:
        form = CreatePost(request.POST)
        if form.is_valid():
            form.save()
        return redirect(recruiterDashboard)
    return render(request, 'tindev/createPost.html', {'form':CreatePost})   
	