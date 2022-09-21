from django.test import TestCase
from django.urls import reverse

from forum.models import Theme, Publication, Comment
from django.contrib.auth import get_user_model


class ForumTestCase(TestCase):
    def setUp(self):
        self.author_of_question = get_user_model().objects.create_user(
            username='testuser',
            password='testuser12345678'
        )
        self.author_of_comment = get_user_model().objects.create_user(
            username='testuser2',
            password='testuser12345678'
        )
        self.theme = Theme.objects.create(
            name='test theme',
        )
        self.publication = Publication.objects.create(
            title='Test question',
            content='Content of test question',
            author=self.author_of_question,
            theme=self.theme,
        )
        self.comment = Comment.objects.create(
            content='Test comment',
            post=self.publication,
            author=self.author_of_comment
        )

    def test_string_representation(self):
        post = Publication(title='Test title')
        self.assertEqual(str(post), post.title)

    def test_get_absolute_url(self):
        self.assertEqual(self.publication.get_absolute_url(), '/post/test-question/')

    def test_post_content(self):
        self.assertEqual(f'{self.publication.title}', 'Test question')
        self.assertEqual(f'{self.publication.author}', self.author_of_question.username)
        self.assertEqual(f'{self.publication.content}', 'Content of test question')

    def test_post_list_view(self):
        response = self.client.get(reverse('main'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Content of test question')
        self.assertTemplateUsed(response, 'forum/index.html')

    def test_post_detail_view(self):
        response = self.client.get('/post/test-question/')
        self.assertEqual(response.status_code, 200)
        no_response = self.client.get('/post/100000/')
        # print(no_response.status_code)
        self.assertEqual(no_response.status_code, 404)
        self.assertContains(response, 'Test question')
        self.assertTemplateUsed(response, 'forum/post.html')

    def test_post_create_view(self):
        response = self.client.post('login/', {'username': 'testuser', 'password': 'testuser12345678'})

        response = self.client.post(reverse('start_question'), {
            'title': 'New title',
            'content': 'New text',
            'theme': self.theme,
        })
        self.assertEqual(response.status_code, 302)
