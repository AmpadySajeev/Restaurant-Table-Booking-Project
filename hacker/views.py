from django.shortcuts import render

# Create your views here.

def landingpage(request):
    return render(request, 'hacker/landing.html')
