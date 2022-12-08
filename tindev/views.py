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
import datetime, re
from django.template.defaulttags import register


# logout view function, displays logout message
def logout_view(request):
    del request.session["logged_user"]
    messages.info(request, 'You have successfully logged out!')
    return redirect('home')


# login view function for user
# only users that match either a candidate or recruiter profile can login
# upon login candidates and recruiters are redirected to respective pages, and dont have access to eachothers pages
def user_login(request):

    if request.POST:

        # get form info
        username = request.POST.get('username')
        password = request.POST.get('password')
        user_type = request.POST.get('profile')

        # check user type
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

        # check user type
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


# view function for creating the candidate profile
# use a form to add candidateProfile object to the database
def candidateProfile(request):
    if request.POST:
        form = CandidateForm(request.POST)
        if form.is_valid():
            form.save()
        return redirect(user_login)
    return render(request, 'tindev/candidateProfile.html', {'form':CandidateForm}) 


# view function for creating the recruiter profile
# use a form to add recruiterProfile object to the database
def recruiterProfile(request):
    if request.POST:
        form = RecruiterForm(request.POST)
        if form.is_valid():
            form.save()
        return redirect(user_login)
    return render(request, 'tindev/recruiterProfile.html', {'form':RecruiterForm}) 


# simple home function, renders the html home page
def home(request):
    return render(request, 'tindev/home.html')


# view function for a recruiter to create a post
# use a form to add job post object to the database
def createPost(request):
    if request.POST:
        form = CreatePostForm(request.POST)
        if form.is_valid():
            job = form.save(commit=False)
            job.recruiter = RecruiterProfile.objects.get(username=request.session["logged_user"])
            job.save()
        return redirect(recruiterDashboard)
    return render(request, 'tindev/createpost.html', {'form':CreatePostForm})


# get interested positions according to logged user and display them
def interestedPositions(request):

    # get current profile from database
    candidate_id = request.session['id']
    candidate_object = CandidateProfile.objects.get(pk = candidate_id)

    interested_jobs = candidate_object.interested.all()

    return render(request, 'tindev/interested.html', {'interested_jobs':interested_jobs})


# render offers html page, acording to the logged user offer (if he/she has any )
def offers(request):

    offers = Offers.objects.filter(candidate=request.session["id"]).all()

    return render(request, 'tindev/offers.html', {'offers':offers, 'today':datetime.date.today()})



# according to user choice, accept or decline job offer
def offerDecision(request, post_id):
    
    # use post request for the form
    if request.POST:

        # get decision value, 1 for accepted and 2 for denied
        decision = request.POST.get("decision_btn")

        # check of accepted
        if decision == '1':
            # match the job offer to the current job's id (passed into the function)
            job = Offers.objects.get(pk=post_id)
            # change the offer status to True (accepted)
            job.acepted = True
            # save the updated model
            job.save()
            
        else:
            # match the job offer to the current job's id (passed into the function)
            job = Offers.objects.get(pk=post_id)
            # change the offer status to False (declined)
            job.acepted = False
            # save the updated modelz
            job.save()

        # redirect to candidate profile
        return redirect(offers)
    else:
        return redirect(offers)


# render cadidate dashboard, with available job postings
# allow for filtering of job postings
def candidateDashboard(request):

    if request.POST:

        # get form entries
        search = request.POST.get("search")
        keyword = request.POST.get("keyword")

        # check filter input
        if search == 'inactive-posts':
            jobPosts = CreatePost.objects.filter(is_active = False)
            return render(request, 'tindev/candidateDashboard.html', {'jobPosts':jobPosts, 'searchTerm':search})
        elif search == 'active-posts':

            jobPosts = CreatePost.objects.filter(is_active = True)

            return render(request, 'tindev/candidateDashboard.html', {'jobPosts':jobPosts, 'searchTerm':search})
        elif search == 'posts_based_on_keywords':

            jobPosts = CreatePost.objects.all()

            posts = {}

            postName = 'post'

            for job in jobPosts:
                postName = 'post'
                if (re.search(keyword, job.description) != None):
                    postName = postName + str(job.id)
                    posts[postName] = job

            return render(request, 'tindev/candidateDashboard.html', {'jobPosts':posts, 'searchTerm':search})
        elif search == 'posts_based_on_location':

            # pass specific filtered jobs to the page using dict and render function

            jobPosts = CreatePost.objects.all()

            posts = {}

            postName = 'post'

            for job in jobPosts:
                postName = 'post'
                if (re.search(keyword, job.location) != None):
                    postName = postName + str(job.id)
                    posts[postName] = job

            return render(request, 'tindev/candidateDashboard.html', {'jobPosts':posts, 'searchTerm':search})
        else:
            jobPosts = CreatePost.objects.all()
           
            return render(request, 'tindev/candidateDashboard.html', {'jobPosts':jobPosts, 'searchTerm':search})

    search = "all-posts"
    jobPosts = CreatePost.objects.all()

    return render(request, 'tindev/candidateDashboard.html', {'jobPosts':jobPosts, 'searchTerm':search})


# render recruiter dashboard, with available job postings
# allow for filtering of job postings
def recruiterDashboard(request):

    candidates = CandidateProfile.objects.all()
    jobPosts = CreatePost.objects.filter(recruiter=request.session['id'])
    totalInterested = {}
    for job in  jobPosts:
        totalInterested[job.id] = len(CandidateProfile.objects.filter(interested__id = job.id))
                
    if request.POST:
        search = request.POST.get("search")
        # check filter input
        if search == 'inactive-posts':
            jobPosts = CreatePost.objects.filter(recruiter=request.session['id'])
            post = jobPosts.filter(is_active = False)
            return render(request, 'tindev/recruiterDashboard.html', {'jobPosts':post, 'searchTerm':search, 'totalInterested':totalInterested})
        elif search == 'active-posts':
            jobPosts = CreatePost.objects.filter(recruiter=request.session['id'])

            post = jobPosts.filter(is_active = True)

            return render(request, 'tindev/recruiterDashboard.html', {'jobPosts':post, 'searchTerm':search, 'totalInterested':totalInterested})
        elif search == 'interested-candidates-posts':
            jobPosts = CreatePost.objects.filter(recruiter=request.session['id'])
            posts = {}
            postName = 'post'
            for job in jobPosts:
                postName = 'post'
                if (CandidateProfile.objects.filter(interested__id = job.id)):
                    postName = postName + str(job.id)
                    posts[postName] = job

            return render(request, 'tindev/recruiterDashboard.html', {'jobPosts':posts, 'searchTerm':search, 'totalInterested':totalInterested})
        else:
            jobPosts = CreatePost.objects.filter(recruiter=request.session['id'])
           
            return render(request, 'tindev/recruiterDashboard.html', {'jobPosts':jobPosts, 'searchTerm':search})

    search = "all-posts"

    return render(request, 'tindev/recruiterDashboard.html', {'jobPosts':jobPosts, 'searchTerm':search, 'totalInterested':totalInterested})


# interes or not interested button logic
# if interested add post object to candidates many to many 'interested' field
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


# logic for the recruiter to be able to edit job posts
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


# logic for recruiter to delete posts he made
def deletePost(request, post_id):

    post = CreatePost.objects.get(id=post_id)
    post.delete()

    return redirect(recruiterDashboard)

# function to allow recruiter to make offer to candidate
# creating offer object and linking it to candidate and job object
def makeoffer(request, post_id):

    interested = CandidateProfile.objects.filter(interested__id=post_id)
    current = CreatePost.objects.get(id = post_id)
    vals = {}

    for i in interested:
        count = 0
        if i.years_experience > '2':
            count += 1
        if re.search(current.preferred_skills, i.skills):
            count += 2
        if re.search(current.preferred_skills, i.bio):
            count += 1
        vals[i.name] = (count/4)*100

    if request.POST:
        form = OffersForm(request.POST)
        if form.is_valid():
            job = form.save(commit=False)
            name = str(request.POST.get('candidates'))
            user_name = CandidateProfile.objects.get(name=name).username
            job.candidate = CandidateProfile.objects.get(username=user_name)
            job.job = CreatePost.objects.get(id=post_id)
            job.save()
        return redirect(recruiterDashboard)
    
    return render(request, 'tindev/makeoffer.html', {'form':OffersForm, "interested":interested, 'jobID':post_id, "vals":vals})
