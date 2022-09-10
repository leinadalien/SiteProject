from django.http import HttpResponse
from django.shortcuts import render
from .models import *

menu = ["About", "log in"]


# Create your views here.
def index(request):
    posts = Publication.objects.all()
    return render(request, 'forum/index.html', {'posts': posts, 'menu': menu, 'title': 'Main'})


def categories(request, cat):
    return HttpResponse(f"Category num {cat}")


def about(request):
    return render(request, 'forum/about.html', {'menu': menu, 'title': 'About'})
