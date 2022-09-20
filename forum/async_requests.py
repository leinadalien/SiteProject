from forum.models import *
from asgiref.sync import sync_to_async


@sync_to_async
def get_all_publications():
    return Publication.objects.filter(is_published=True)


@sync_to_async
def get_publications_by_theme(theme_slug):
    return Publication.objects.filter(theme__slug=theme_slug, is_published=True)


@sync_to_async
def get_my_questions(user):
    return Publication.objects.filter(author=user)