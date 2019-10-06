from django.shortcuts import render, redirect
from datetime import datetime, timedelta, timezone
from .models import Dictionary, Part, Posts, Reply
from user.models import User

# Create your views here.

def index(request):
    
    return render(request, 'bbs/index.html')

def teahouse(request):
    
    return render(request, 'bbs/index.html')