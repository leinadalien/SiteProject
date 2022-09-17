from django.urls import path

from .views import *

urlpatterns = [
    path('', ForumHome.as_view(), name='main'),
    path('about/', about, name='about'),
    path('login/', LoginUser.as_view(), name='login'),
    path('logout/', logout_user, name='logout'),
    path('register/', RegisterUser.as_view(), name='register'),
    path('post/<slug:post_slug>/', ShowPost.as_view(), name='post'),
    path('theme/<slug:theme_slug>/', PublicationByTheme.as_view(), name='theme'),
    path('start-question/', StartQuestion.as_view(), name='start_question'),
    path('my-questions/', MyQuestions.as_view(), name='my_questions'),
    path('delete-post/<slug:post_slug>/', delete_post, name='delete_post'),
    path('close-post/<slug:post_slug>/', close_post, name='close_post'),
]
