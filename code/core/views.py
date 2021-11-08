from django.shortcuts import render
from django.conf import settings

def homepage(request):
    ctx={}
    ctx['redirect_url']=settings.BASE_URL
    return render(request, 'home.html',ctx)