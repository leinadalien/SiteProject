from django.http import HttpResponse, Http404
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView
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


def show_post(request, post_slug):
    post = get_object_or_404(Publication, slug=post_slug)
    themes = Theme.objects.all()
    context = {
        'post': post,
        'menu': menu,
        'title': post.title,
        'themes': themes,
        'theme_selected': post.theme.slug
    }
    return render(request, 'forum/post.html', context=context)


class PublicationByTheme(ListView):
    model = Publication
    template_name = 'forum/index.html'
    context_object_name = 'posts'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['menu'] = menu
        context['title'] = 'Главная'
        context['themes'] = Theme.objects.all()
        context['theme_selected'] = 0  #need change
        return context

    def get_queryset(self):
        return Publication.objects.filter(theme__slug=self.kwargs['theme_slug'], is_published=True)


def show_theme(request, theme_slug):
    theme = get_object_or_404(Theme, slug=theme_slug)
    posts = Publication.objects.filter(theme=theme)
    themes = Theme.objects.all()

    if len(posts) == 0:
        raise Http404()
    context = {
        'posts': posts,
        'themes': themes,
        'theme_selected': theme.pk,
        'menu': menu,
        'title': theme
    }
    return render(request, 'forum/index.html', context=context)


def start_question(request):
    if request.method == 'POST':
        form = StartThemeForm(request.POST)
        if form.is_valid():
            form.save()
            return index(request)
    else:
        form = StartThemeForm()
    context = {
        'form': form,
        'menu': menu,
        'title': 'Создание Вопроса',
        'themes': Theme.objects.all()
    }
    return render(request, 'forum/start_question.html', context=context)


def my_questions(request):
    return HttpResponse("my questions")
