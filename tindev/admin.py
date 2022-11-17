from django.contrib import admin

# Register your models here.

from .models import CandidateProfile
from .models import RecruiterProfile

admin.site.register(CandidateProfile)

admin.site.register(RecruiterProfile)