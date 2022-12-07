from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.views.generic import ListView, DetailView
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from tindev.forms import CandidateForm, RecruiterForm, CreatePostForm, OffersForm
from tindev.models import CandidateProfile, RecruiterProfile, CreatePost, Offers
import datetime


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
            if len(list(candidate)) == 0:
                context = {'error':'Invalid username, password or position'}
                return render(request, 'tindev/login.html', context)   
            else:
                request.session["logged_user"] = username
                request.session["id"] = CandidateProfile.objects.get(username=username).id
                request.session["role"] = "Candidate"
                return redirect(candidateDashboard)

        elif user_type == 'Recruiter':
            recruiter = RecruiterProfile.objects.filter(username=username, password=password)
            if len(list(recruiter)) == 0:   
                context = {'error':'Invalid username, password or position'}
                return render(request, 'tindev/login.html', context)
            else:
                request.session["logged_user"] = username
                request.session["role"] = "Recruiter"
                request.session["id"] = RecruiterProfile.objects.get(username=username).id

                jobPosts = CreatePost.objects.filter(recruiter=request.session['id'])

                for i in jobPosts:
                    if i.expiration_date < datetime.date.today():
                        i.is_active = 'False'
                        i.save()
                    else:
                        i.is_active = 'True'
                        i.save()
                
                return redirect(recruiterDashboard)
        else:
            context = {'error':'Must select a user_type'}
            return render(request, 'tindev/login.html', context)

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
            job = form.save(commit=False)
            job.recruiter = RecruiterProfile.objects.get(username=request.session["logged_user"])
            job.save()
        return redirect(recruiterDashboard)
    return render(request, 'tindev/createpost.html', {'form':CreatePostForm})


##########################################################################
####################### DASHBOARDS / VIEWING POSTS #######################
##########################################################################

def interestedPositions(request):

    # get current profile from database
    candidate_id = request.session['id']
    candidate_object = CandidateProfile.objects.get(pk = candidate_id)

    interested_jobs = candidate_object.interested.all()

    return render(request, 'tindev/interested.html', {'interested_jobs':interested_jobs})

def offers(request):

    return render(request, 'tindev/offers.html')


def candidateDashboard(request):

    jobPosts = CreatePost.objects.all()

    return render(request, 'tindev/candidateDashboard.html', {'jobPosts':jobPosts})


def recruiterDashboard(request):

    jobPosts = CreatePost.objects.filter(recruiter=request.session['id'])

    return render(request, 'tindev/recruiterDashboard.html', {'jobPosts':jobPosts})


def interested(request): 
    if request.POST:

        interested_val = request.POST.get("interested_val")
        if interested_val == '2':
            # get candidate
            candidate_id = request.session["id"]
            candidate = CandidateProfile.objects.get(pk = candidate_id)

            # get job
            job_id = request.session.get('posts_id')
            job = CreatePost.objects.get(pk = job_id)

            # add job to candidate profile (many-to-many relationship)
            candidate.interested.remove(job)
            candidate.save()

            # redirect to candidate profile
            return redirect(candidateDashboard)
        else:
            # get candidate
            candidate_id = request.session["id"]
            candidate = CandidateProfile.objects.get(pk = candidate_id)

            # get job
            job_id = request.session.get('posts_id')
            job = CreatePost.objects.get(pk = job_id)

            # add job to candidate profile (many-to-many relationship)
            candidate.interested.add(job)
            candidate.save()

            # redirect to candidate profile
            return redirect(candidateDashboard)
    else:
        return redirect(recruiterDashboard)

# Use ListView to display all of the job postings saved within the Django database
class ViewPostings(ListView):

    # Initialize HTML template name
    template_name = 'tindev/post.html'

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
    template_name = 'tindev/post.html'

def detail(request, post_id):
    post = CreatePost.objects.get(pk=post_id) # get post objects for specific blog entry
    request.session['posts_id'] = post_id
    return render(request, 'tindev/post.html', {'post': post}) # route to results html page 

def detail_r(request, post_id):
    post = CreatePost.objects.get(pk=post_id) # get post objects for specific blog entry
    request.session['posts_id'] = post_id
    return render(request, 'tindev/post_recruiter.html', {'post': post}) # route to results html page 

def editPost(request, post_id):

    post = CreatePost.objects.get(id=post_id)

    if request.method == 'POST':
        form = CreatePostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
        jobPosts = CreatePost.objects.filter(recruiter=request.session['id'])

        for i in jobPosts:
            if i.expiration_date < datetime.date.today():
                i.is_active = 'False'
                i.save()
            else:
                i.is_active = 'True'
                i.save()
        return redirect(recruiterDashboard)
    else:
        form = CreatePostForm(instance=post)

    return render(request, 'tindev/editPost.html', {'form':form})



def deletePost(request, post_id):

    post = CreatePost.objects.get(id=post_id)
    post.delete()

    return redirect(recruiterDashboard)


def makeOffer(request, post_id):
    interested = CandidateProfile.objects.filter(interested__id=post_id)

    if request.POST:
        form = OffersForm(request.POST)
        if form.is_valid():
            form.save()
        return redirect(user_login)
    return render(request, 'tindev/makeOffer.html', {'form':OffersForm, "interested":interested})

def passOffer(request, post_id):

    print('hi')

    return render(request, 'tindev/home.html')