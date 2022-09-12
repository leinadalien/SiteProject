from django.http import HttpResponse, Http404
from django.shortcuts import render, get_object_or_404
from .models import *

menu = [
    {'title': 'About', 'url_name': 'about'},
    {'title': 'Log in', 'url_name': 'login'}
]


# Create your views here.
def index(request):
    posts = Publication.objects.all()
    themes = Theme.objects.all()
    context = {
        'posts': posts,
        'themes': themes,
        'theme_selected': 0,
        'menu': menu,
        'title': 'Main'
    }
    return render(request, 'forum/index.html', context=context)


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
