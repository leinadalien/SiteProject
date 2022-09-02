from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
def index(request):
    return HttpResponse("Forum page")

def categories(request, cat):
    return HttpResponse(f"Category num {cat}")