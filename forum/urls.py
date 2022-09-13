from django.urls import path

from .views import *

urlpatterns = [
    path('', ForumHome.as_view(), name='main'),
    path('about/', about, name='about'),
    path('login/', login, name='login'),
    path('post/<slug:post_slug>/', show_post, name='post'),
    path('theme/<slug:theme_slug>/', PublicationByTheme.as_view(), name='theme'),
    path('start-question/', start_question, name='start_question'),
    path('my-questions/', my_questions, name='my_questions')
]
