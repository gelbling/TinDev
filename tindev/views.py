from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from tindev.forms import CandidateForm
from tindev.models import CandidateProfile
from tindev.forms import RecruiterForm
from tindev.models import RecruiterProfile
from tindev.forms import CreatePost
from django.views.generic import ListView, DetailView
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User

from .models import CreatePost


def logout_view(request):
    logout(request)
    messages.info(request, 'You have successfully logged out!')
    return redirect('home')


def user_login(request):

    if request.POST:

        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is None:
            context = {'error':'Invalid username or password'}
            return render(request, 'tindev/login.html', context)

        login(request,user)
        return render(request, 'tindev/home.html')

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


def createPost(request):
    if request.POST:
        form = CreatePost(request.POST)
        if form.is_valid():
            form.save()
        return redirect(recruiterDashboard)
    return render(request, 'tindev/createPost.html', {'form':CreatePost})


##########################################################################
####################### DASHBOARDS / VIEWING POSTS #######################
##########################################################################


def candidateDashboard(request):

    jobPosts = CreatePost.objects.all()

    return render(request, 'tindev/candidateDashboard.html', {'jobPosts':jobPosts})


def recruiterDashboard(request):

    jobPosts = CreatePost.objects.all()

    return render(request, 'tindev/recruiterDashboard.html', {'jobPosts':jobPosts})


# Use ListView to display all of the job postings saved within the Django database
class ViewPostings(ListView):

    # Initialize HTML template name
    template_name = 'tindev/recruiterDashboard.html'

    # Initialize the reference name for the job posts
    context_object_name = 'job_posts'

    # Use get_queryset function to order posts by publication date
    def get_queryset(self):
        return CreatePost.objects.order_by('expiration_date')


# Use DetailView to display the content and details of the job posts
class PostContents(DetailView):
    
    # Initialize blog
    model = CreatePost

    # Initialize the HTML template name
    #template_name = 'tindev/recruiterDashboard.html'


	