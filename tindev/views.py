from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from tindev.forms import CandidateForm
from tindev.models import CandidateProfile


def login(request):
    return render(request, 'tindev/login.html')

def candidateProfile(request):
    if request.POST:
        form = CandidateForm(request.POST)
        if form.is_valid():
            form.save()
        return redirect(login)
    return render(request, 'tindev/candidateProfile.html', {'form':CandidateForm}) 