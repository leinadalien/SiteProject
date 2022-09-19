from forum.models import *


not_auth_menu = [
    {'title': 'Главная', 'url_name': 'main'},
    {'title': 'О сайте', 'url_name': 'about'},
    {'title': 'Войти', 'url_name': 'login'},
    {'title': 'Регистрация', 'url_name': 'register'}
]
usual_menu = [
    {'title': 'Главная', 'url_name': 'main'},
    {'title': 'О сайте', 'url_name': 'about'},
    {'title': 'Создать вопрос', 'url_name': 'start_question'},
    {'title': 'Мои вопросы', 'url_name': 'my_questions'},
    {'title': 'Выйти', 'url_name': 'logout'}
]


class DataMixin:
    def get_user_context(self, **kwargs):
        context = kwargs
        themes = Theme.objects.all()
        if self.request.user.is_authenticated:
            context['menu'] = usual_menu
        else:
            context['menu'] = not_auth_menu
        context['themes'] = themes
        return context
