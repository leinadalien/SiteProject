from django.http import HttpResponse, Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView
from .forms import *
from .models import *

menu = [
    {'title': 'О сайте', 'url_name': 'about'},
    {'title': 'Создать вопрос', 'url_name': 'start_question'},
    {'title': 'Мои вопросы', 'url_name': 'my_questions'},
    {'title': 'Войти', 'url_name': 'login'}
]


class ForumHome(ListView):
    model = Publication
    template_name = 'forum/index.html'
    context_object_name = 'posts'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['menu'] = menu
        context['title'] = 'Главная'
        context['themes'] = Theme.objects.all()
        context['theme_selected'] = 0
        return context

    def get_queryset(self):
        return Publication.objects.filter(is_published=True)


def categories(request, cat):
    return HttpResponse(f"Category num {cat}")


def about(request):
    return render(request, 'forum/about.html', {'menu': menu, 'title': 'About'})


def login(request):
    return HttpResponse('log in')


class ShowPost(DetailView):
    model = Publication
    template_name = 'forum/post.html'
    slug_url_kwarg = 'post_slug'
    context_object_name = 'post'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['menu'] = menu
        context['title'] = context['post']
        context['themes'] = Theme.objects.all()
        return context


class PublicationByTheme(ListView):
    model = Publication
    template_name = 'forum/index.html'
    context_object_name = 'posts'
    allow_empty = False

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['menu'] = menu
        context['title'] = context['posts'][0].theme
        context['themes'] = Theme.objects.all()
        context['theme_selected'] = context['posts'][0].theme_id
        return context

    def get_queryset(self):
        return Publication.objects.filter(theme__slug=self.kwargs['theme_slug'], is_published=True)


class StartQuestion(CreateView):
    form_class = StartQuestionForm
    template_name = 'forum/start_question.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['menu'] = menu
        context['title'] = 'Создание вопроса'
        context['themes'] = Theme.objects.all()
        return context


def my_questions(request):
    return HttpResponse("my questions")
