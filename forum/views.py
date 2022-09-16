from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse, Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import *
from .models import *
from .utils import *


class ForumHome(DataMixin, ListView):
    model = Publication
    template_name = 'forum/index.html'
    context_object_name = 'posts'
    paginate_by = 3

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(self.get_user_context())
        context['theme_selected'] = 0
        context['title'] = 'Главная'
        return context

    def get_queryset(self):
        return Publication.objects.filter(is_published=True)


def about(request):
    return render(request, 'forum/about.html', {'title': 'About'})


def login(request):
    return HttpResponse('log in')


class ShowPost(DataMixin, DetailView):
    model = Publication
    template_name = 'forum/post.html'
    slug_url_kwarg = 'post_slug'
    context_object_name = 'post'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(self.get_user_context())
        context['title'] = context['post']
        return context


class PublicationByTheme(DataMixin, ListView):
    model = Publication
    template_name = 'forum/index.html'
    context_object_name = 'posts'
    allow_empty = False
    paginate_by = 3

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(self.get_user_context())
        context['title'] = context['posts'][0].theme
        context['theme_selected'] = context['posts'][0].theme_id
        return context

    def get_queryset(self):
        return Publication.objects.filter(theme__slug=self.kwargs['theme_slug'], is_published=True)


class StartQuestion(LoginRequiredMixin, DataMixin, CreateView):
    form_class = StartQuestionForm
    template_name = 'forum/start_question.html'
    login_url = reverse_lazy('login')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(self.get_user_context())
        context['title'] = 'Создание вопроса'
        return context


class RegisterUser(DataMixin, CreateView):
    form_class = RegisterUserForm
    template_name = 'forum/register.html'
    success_url = reverse_lazy('login')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(self.get_user_context())
        context['title'] = 'Регистрация'
        return context


def my_questions(request):
    return HttpResponse("my questions")
