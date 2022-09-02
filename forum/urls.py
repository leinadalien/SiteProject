from django.urls import path

from .views import *

urlpatterns = [
    path('', index, name='main'),
    path('categories/<slug:cat>/', categories),
]