from django.urls import path, include
from . import views

urlpatterns = [
    #path('', views.index),  #the path for our index view
    path('candidateprofile/', views.candidateProfile, name='CandidateProfile'),
    path('recruiterprofile/', views.recruiterProfile, name='RecruiterProfile'),
    path('login/', views.user_login, name='login'),
    path('', views.home, name='home'),
    path('users/', include("django.contrib.auth.urls"))
]