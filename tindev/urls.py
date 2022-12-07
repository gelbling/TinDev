from django.urls import path, include
from . import views

urlpatterns = [
    path('candidateprofile/', views.candidateProfile, name='CandidateProfile'),
    path('recruiterprofile/', views.recruiterProfile, name='RecruiterProfile'),
    path('login/', views.user_login, name='login'),
    path('', views.home, name='home'),
    path('users/', include("django.contrib.auth.urls")),
    path('candidatedashboard/', views.candidateDashboard, name='CandidateDashboard'),
    path('recruiterdashboard/', views.recruiterDashboard, name='RecruiterDashboard'),
    path('createpost/', views.createPost, name='CreatePost'),
    path('logout/', views.logout_view, name='logout'),
    path('<int:post_id>/', views.detail, name='detail'),
    path('interested/', views.interested, name='interested'),
    path('interestedpositions/', views.interestedPositions, name='InterestedPositions'),
    path('offers/', views.offers, name='Offers'),
    path('<int:post_id>/change/', views.editPost, name='change'),
    path('<int:post_id>/delete/', views.deletePost, name='delete'),
    path('<int:post_id>/offer/', views.makeOffer, name='offer')
]