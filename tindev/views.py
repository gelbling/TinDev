from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.views.generic import ListView, DetailView
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from tindev.forms import CandidateForm, RecruiterForm, CreatePostForm
from tindev.models import CandidateProfile, RecruiterProfile, CreatePost


def logout_view(request):
    del request.session["logged_user"]
    messages.info(request, 'You have successfully logged out!')
    return redirect('home')


def user_login(request):

    if request.POST:

        username = request.POST.get('username')
        password = request.POST.get('password')
        user_type = request.POST.get('profile')

        if user_type == 'Candidate':
            candidate = CandidateProfile.objects.filter(username=username, password=password) 
            if list(candidate) == 0:
                context = {'error':'Invalid username or password'}
                return render(request, 'tindev/login.html', context)   
            else:
                request.session["logged_user"] = username
                request.session["id"] = CandidateProfile.objects.get(username=username).id
                request.session["role"] = "Candidate"
                return redirect(candidateDashboard)

        elif user_type == 'Recruiter':
            recruiter = RecruiterProfile.objects.filter(username=username, password=password)
            if list(recruiter) == 0:   
                context = {'error':'Invalid username or password'}
                return render(request, 'tindev/login.html', context)
            else:
                request.session["logged_user"] = username
                request.session["role"] = "Recruiter"
                request.session["id"] = RecruiterProfile.objects.get(username=username).id
                return redirect(recruiterDashboard)

    return render(request, 'tindev/login.html')



def candidateProfile(request):
    if request.POST:
        form = CandidateForm(request.POST)
        if form.is_valid():
            form.save()
        return redirect(user_login)
    return render(request, 'tindev/candidateProfile.html', {'form':CandidateForm}) 



def recruiterProfile(request):
    if request.POST:
        form = RecruiterForm(request.POST)
        if form.is_valid():
            form.save()
        return redirect(user_login)
    return render(request, 'tindev/recruiterProfile.html', {'form':RecruiterForm}) 


def home(request):
    return render(request, 'tindev/home.html')


def createPost(request):
    if request.POST:
        form = CreatePostForm(request.POST)
        if form.is_valid():
            form.save()
        return redirect(recruiterDashboard)
    return render(request, 'tindev/createpost.html', {'form':CreatePostForm})


##########################################################################
####################### DASHBOARDS / VIEWING POSTS #######################
##########################################################################


def candidateDashboard(request):

    jobPosts = CreatePost.objects.all()

    return render(request, 'tindev/candidateDashboard.html', {'jobPosts':jobPosts})


def recruiterDashboard(request):

    jobPosts = CreatePost.objects.all()

    return render(request, 'tindev/recruiterDashboard.html', {'jobPosts':jobPosts})

def interested(request): # FIX BUT SOMEWHAT THIS
    candidate_id = request.session["id"]
    candidate = candidate.objects.get(pk = id)
    job = job.objects.get(pk = job_id)
    candidate.interested.add(job)
    candidate.save()

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



	