from django.contrib.auth import logout, login
from django.contrib.auth.views import LoginView
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import *
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import FormMixin
import logging
from .forms import *
from .models import *
from .utils import *

logger = logging.getLogger('main')


class ForumHome(DataMixin, ListView):
    model = Publication
    template_name = 'forum/index.html'
    context_object_name = 'posts'
    allow_empty = True
    paginate_by = 5

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(self.get_user_context())
        context['theme_selected'] = 0
        context['title'] = 'Главная'
        context['menu_item_selected'] = 'main'
        return context

    def get_queryset(self):
        return Publication.objects.filter(is_published=True)


def about(request):
    context = {
        'title': 'О сайте',
        'themes': Theme.objects.all(),
        'menu_item_selected': 'about'
    }
    if request.user.is_authenticated:
        context['menu'] = usual_menu
    else:
        context['menu'] = not_auth_menu
    return render(request, 'forum/about.html', context=context)


class ShowPost(FormMixin, DataMixin, DetailView):
    model = Publication
    template_name = 'forum/post.html'
    slug_url_kwarg = 'post_slug'
    context_object_name = 'post'
    form_class = AddCommentForm

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(self.get_user_context())
        context['title'] = context['post']
        return context

    def get_success_url(self):
        return reverse_lazy('post', kwargs={'post_slug': self.object.slug})

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        logger.info('Добавление комментария')
        post = self.get_object()
        new_comment = form.save(commit=False)
        new_comment.post = post
        new_comment.author = self.request.user
        new_comment.save()
        return super(ShowPost, self).form_valid(form)


class PublicationByTheme(DataMixin, ListView):
    model = Publication
    template_name = 'forum/index.html'
    context_object_name = 'posts'
    allow_empty = True
    paginate_by = 5

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(self.get_user_context())
        context['title'] = kwargs['theme_name'].name
        context['theme_selected'] = kwargs['theme_name'].slug
        return context

    def get_queryset(self):
        return Publication.objects.filter(theme__slug=self.kwargs['theme_slug'], is_published=True)

    def get(self, request, *args, **kwargs):
        self.object_list = self.get_queryset()
        allow_empty = self.get_allow_empty()

        if not allow_empty:
            # When pagination is enabled and object_list is a queryset,
            # it's better to do a cheap query than to load the unpaginated
            # queryset in memory.
            if self.get_paginate_by(self.object_list) is not None and hasattr(
                    self.object_list, "exists"
            ):
                is_empty = not self.object_list.exists()
            else:
                is_empty = not self.object_list
            if is_empty:
                raise Http404(
                    _("Empty list and “%(class_name)s.allow_empty” is False.")
                    % {
                        "class_name": self.__class__.__name__,
                    }
                )
        context = self.get_context_data(theme_name=get_object_or_404(Theme, slug=self.kwargs['theme_slug']))
        return self.render_to_response(context)


class StartQuestion(LoginRequiredMixin, DataMixin, CreateView):
    form_class = StartQuestionForm
    template_name = 'forum/start_question.html'
    login_url = reverse_lazy('login')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(self.get_user_context())
        context['title'] = 'Создание вопроса'
        context['menu_item_selected'] = 'start_question'
        return context

    def form_valid(self, form):
        logger.info('Создание вопроса')
        new_post = form.save(commit=False)
        new_post.author = self.request.user
        new_post.save()
        return redirect('post', new_post.slug)


class RegisterUser(DataMixin, CreateView):
    form_class = RegisterUserForm
    template_name = 'forum/register.html'
    success_url = reverse_lazy('login')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(self.get_user_context())
        context['title'] = 'Регистрация'
        context['menu_item_selected'] = 'register'
        return context

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('main')


class LoginUser(DataMixin, LoginView):
    form_class = AuthenticationForm
    template_name = 'forum/login.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(self.get_user_context())
        context['title'] = 'Вход'
        context['menu_item_selected'] = 'login'
        return context

    def get_success_url(self):
        return reverse_lazy('main')


def logout_user(request):
    logger.info('Выход из системы')
    logout(request)
    return redirect('main')


class MyQuestions(DataMixin, ListView):
    model = Publication
    template_name = 'forum/my_questions.html'
    context_object_name = 'posts'
    allow_empty = True
    paginate_by = 5

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(self.get_user_context())
        context['title'] = 'Мои вопросы'
        context['menu_item_selected'] = 'my_questions'
        return context

    def get_queryset(self):
        return Publication.objects.filter(author=self.request.user)


def delete_post(request, post_slug):
    post = get_object_or_404(Publication, slug=post_slug)
    if request.user == post.author or request.user.is_staff:
        logger.info('удаление поста')
        post.delete()
        return redirect('my_questions')
    else:
        raise Http404


def close_post(request, post_slug):
    post = get_object_or_404(Publication, slug=post_slug)
    if not post.closed and (request.user == post.author or request.user.is_staff):
        logger.info('закрытие поста')
        post.closed = True
        post.save()
        return redirect('post', post_slug)
    else:
        raise Http404


class AddTheme(LoginRequiredMixin, DataMixin, CreateView):
    form_class = AddThemeForm
    template_name = 'forum/add_theme.html'
    login_url = reverse_lazy('add_theme')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(self.get_user_context())
        context['title'] = 'Добавление темы'
        return context

    def form_valid(self, form):
        if self.request.user.is_staff:
            logger.info('Создание темы')
            new_theme = form.save()
            return redirect('theme', new_theme.slug)
        else:
            raise Http404


def delete_theme(request, theme_slug):
    theme = get_object_or_404(Theme, slug=theme_slug)
    if request.user.is_staff:
        logger.info('удаление темы')
        theme.delete()
        return redirect('main')
    else:
        raise Http404
