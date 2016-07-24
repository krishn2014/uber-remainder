from django.shortcuts import render
from django.http import HttpResponse, Http404
import itertools
import datetime

# importing models
from models import *

# Create your views here.
def root_page (request):
    return HttpResponse ("""API's root url and working!!""")

# Django REST framework
from django.utils import timezone
from django.contrib.auth.models import User, Group

from django import forms

class RemainderForm(forms.ModelForm):

    class Meta:
        model = Remainders
        fields = ('travel_date_time', 'emailid', 'srclat', 'srclong', 'destlat', 'destlong',)

def post_new(request):
    if request.method == "POST":
        form = RemainderForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.save()
    else:
        form = RemainderForm()
    req = Remainders.objects.all()
    return render(request, 'post_edit.html', {'form': form, 'recent_requests': req})
