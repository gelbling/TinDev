from re import A
from django.contrib import admin

# Register your models here.

from .models import CandidateProfile
from .models import RecruiterProfile
from .models import CreatePost

admin.site.register(CandidateProfile)

admin.site.register(RecruiterProfile)

admin.site.register(CreatePost)