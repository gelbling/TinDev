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





def candidateDashboard(request):

    if request.POST:
        search = request.POST.get("search")
        keyword = request.POST.get("keyword")

        if search == 'inactive-posts':
            jobPosts = CreatePost.objects.filter(is_active = False)
            return render(request, 'tindev/candidateDashboard.html', {'jobPosts':jobPosts, 'searchTerm':search})
        elif search == 'active-posts':

            jobPosts = CreatePost.objects.filter(is_active = True)

            return render(request, 'tindev/candidateDashboard.html', {'jobPosts':jobPosts, 'searchTerm':search})
        elif search == 'posts_based_on_keywords':
            #jobPosts = CreatePost.objects.filter(is_active = True)
            #print(re.search(current.preferred_skills, i.skills))
            #j = CreatePost.objects.get().description
            #print(j)
            jobPosts = CreatePost.objects.all()
            return render(request, 'tindev/candidateDashboard.html', {'jobPosts':jobPosts, 'searchTerm':search})
        elif search == 'posts_based_on_location':
            jobPosts = CreatePost.objects.all()
            return render(request, 'tindev/candidateDashboard.html', {'jobPosts':jobPosts, 'searchTerm':search})
        else:
            jobPosts = CreatePost.objects.all()
           
            return render(request, 'tindev/candidateDashboard.html', {'jobPosts':jobPosts, 'searchTerm':search})

    search = "all-posts"
    jobPosts = CreatePost.objects.all()

    return render(request, 'tindev/candidateDashboard.html', {'jobPosts':jobPosts, 'searchTerm':search})


def recruiterDashboard(request):

    if request.POST:
        search = request.POST.get("search")
        if search == 'inactive-posts':
            jobPosts = CreatePost.objects.filter(recruiter=request.session['id'])
            post = jobPosts.filter(is_active = False)
            return render(request, 'tindev/recruiterDashboard.html', {'jobPosts':post, 'searchTerm':search})
        elif search == 'active-posts':
            jobPosts = CreatePost.objects.filter(recruiter=request.session['id'])

            post = jobPosts.filter(is_active = True)

            return render(request, 'tindev/recruiterDashboard.html', {'jobPosts':post, 'searchTerm':search})
        elif search == 'interested-candidates-posts':
            jobPosts = CreatePost.objects.filter(recruiter=request.session['id'])
            posts = {}
            postName = 'post'
            for job in jobPosts:
                postName = 'post'
                if (CandidateProfile.objects.filter(interested__id = job.id)):
                    postName = postName + str(job.id)
                    posts[postName] = job

            totalInterested = len(posts)

            return render(request, 'tindev/recruiterDashboard.html', {'jobPosts':posts, 'searchTerm':search})
        else:
            jobPosts = CreatePost.objects.filter(recruiter=request.session['id'])
           
            return render(request, 'tindev/recruiterDashboard.html', {'jobPosts':jobPosts, 'searchTerm':search})

    search = "all-posts"
    jobPosts = CreatePost.objects.filter(recruiter=request.session['id'])

    return render(request, 'tindev/recruiterDashboard.html', {'jobPosts':jobPosts, 'searchTerm':search})


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

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)

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
