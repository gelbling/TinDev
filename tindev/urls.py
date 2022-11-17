from django.urls import path
from . import views

urlpatterns = [
    #path('', views.index),  #the path for our index view
    path('candidateprofile/', views.candidateProfile, name='CandidateProfile'),
    path('recruiterprofile/', views.recruiterProfile, name='RecruiterProfile'),
    path('', views.login, name='login')
]