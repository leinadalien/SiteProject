from django.db import models
from django.urls import reverse


class Publication(models.Model):
    title = models.CharField(max_length=255, verbose_name="Заголовок")
    content = models.TextField(verbose_name="Содержимое")
    time_create = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    time_update = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")
    is_published = models.BooleanField(default=True, verbose_name="Опубликовано")
    theme = models.ForeignKey('Theme', on_delete=models.PROTECT, verbose_name="Тема")
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL")
    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post', kwargs={'post_slug': self.slug})

    class Meta:
        verbose_name = 'Публикациия'
        verbose_name_plural = 'Публикации'
        ordering = ['-time_create', 'title']


class Theme(models.Model):
    name = models.CharField(max_length=50, db_index=True, verbose_name="Название")
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL")
    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('theme', kwargs={'theme_slug': self.slug})

    class Meta:
        verbose_name = 'Тема'
        verbose_name_plural = 'Темы'
        ordering = ['id']
