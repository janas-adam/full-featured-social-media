import os
from django.test import TestCase
from blog_app.forms import CommentForm
from django.contrib.auth.models import User
from django.test.client import Client
from django.urls import reverse
from django.http import HttpResponse



class BlogTestCase(TestCase):

    client = Client()

    def setUp(self):
        self.user = User.objects.create(
            username='testuser', email='testemail@test.com', password='testpassword')
        os.environ['RECAPTCHA_DISABLE'] = 'True'

    def test_valid_comment_form(self):
        self.client.login(username='testuser', password='testpassword')

        data = {
            'content': 'commentcontent',
        }

        form = CommentForm(data=data)
        self.assertTrue(form.is_valid())

    def tearDown(self):
        del os.environ['RECAPTCHA_DISABLE']

    def test_invalid_comment_form(self):
        self.client.login(username='testuser', password='testpassword')

        data = {
            'content': '',
        }

        form = CommentForm(data=data)
        self.assertFalse(form.is_valid())

