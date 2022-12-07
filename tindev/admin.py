from re import A
from django.contrib import admin

# Register your models here.

from .models import CandidateProfile
from .models import RecruiterProfile
from .models import CreatePost
from .models import Offers


admin.site.register(CandidateProfile)

admin.site.register(RecruiterProfile)

admin.site.register(CreatePost)

admin.site.register(Offers)