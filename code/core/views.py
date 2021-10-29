from django.shortcuts import render


def homepage(request):
    ctx={}
    return render(request, 'home.html',ctx)