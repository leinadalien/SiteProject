from django.urls import path

from .views import *

urlpatterns = [
    path('', index, name='main'),
    path('about/', about, name='about'),
    path('login/', login, name='login'),
    path('post/<slug:post_slug>/', show_post, name='post'),
    path('theme/<slug:theme_slug>/', show_theme, name='theme'),
    path('start-theme/', start_theme, name='start_theme'),
    path('my-themes/', my_themes, name='my_themes')
]
