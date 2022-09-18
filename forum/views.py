from django.contrib.auth import logout, login
from django.contrib.auth.views import LoginView
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import *
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import FormMixin

from .forms import *
from .models import *
from .utils import *


class ForumHome(DataMixin, ListView):
    model = Publication
    template_name = 'forum/index.html'
    context_object_name = 'posts'
    paginate_by = 4

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(self.get_user_context())
        context['theme_selected'] = 0
        context['title'] = 'Главная'
        return context

    def get_queryset(self):
        return Publication.objects.filter(is_published=True)


def about(request):

    context = {
        'title': 'О сайте',
        'themes': Theme.objects.all()
    }
    if request.user.is_authenticated:
        context['menu'] = usual_menu
    else:
        context['menu'] = not_auth_menu
    return render(request, 'forum/about.html', context=context )


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
            #context['form'] = AddCommentForm(initial={'post': self.object})
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

    def form_valid(self, form):
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
        return context

    def get_success_url(self):
        return reverse_lazy('main')


def logout_user(request):
    logout(request)
    return redirect('main')


class MyQuestions(DataMixin, ListView):
    model = Publication
    template_name = 'forum/my_questions.html'
    context_object_name = 'posts'
    allow_empty = False
    paginate_by = 3

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(self.get_user_context())
        context['title'] = 'Мои вопросы'
        return context

    def get_queryset(self):
        return Publication.objects.filter(author=self.request.user)


def delete_post(request, post_slug):
    post = get_object_or_404(Publication, slug=post_slug)
    if request.user == post.author:
        post.delete()
        return redirect('my_questions')
    else:
        raise Http404


def close_post(request, post_slug):
    post = get_object_or_404(Publication, slug=post_slug)
    if request.user == post.author:
        post.closed = True
        post.save()
        return redirect('post', post_slug)
    else:
        raise Http404

