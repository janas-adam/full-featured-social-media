import os
from django.test import TestCase
from users.forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from blog_app.forms import CommentForm
from django.contrib.auth.models import User
from django.test.client import Client
from django.urls import reverse
from django.http import HttpResponse
from django.core.files.uploadedfile import SimpleUploadedFile


class BlogTestCase(TestCase):

    client = Client()

    def setUp(self):
        self.user = User.objects.create(
            username='testuser', email='testemail@test.com', password='testpassword')
        os.environ['RECAPTCHA_DISABLE'] = 'True'

    def test_valid_user_form(self):
        data = {
            'username': 'testuser1',
            'email': 'testemail1@test.com',
            'password1': 'testpassword1',
            'password2': 'testpassword1'
        }

        form = UserRegisterForm(data=data)
        self.assertTrue(form.is_valid())

    def test_invalid_user_form(self):
        data = {
            'username': '',
            'email': 'testemail1@test.com',
            'password1': 'testpassword1',
            'password2': 'testpassword1'
        }

        form = UserRegisterForm(data=data)
        self.assertFalse(form.is_valid())

    def test_valid_comment_form(self):
        data = {
            'content': 'commentcontent',
        }

        form = CommentForm(data=data)
        self.assertTrue(form.is_valid())

    def tearDown(self):
        del os.environ['RECAPTCHA_DISABLE']

    def test_invalid_comment_form(self):
        data = {
            'content': '',
        }

        form = CommentForm(data=data)
        self.assertFalse(form.is_valid())

    def test_valid_user_update_form(self):
        data = {
            'username': 'testuser2',
            'email': 'testemail2@test.com'
        }

        form = UserUpdateForm(data=data)
        self.assertTrue(form.is_valid())

    def test_valid_user_update_form(self):
        data = {
            'username': 'testuser2',
            'email': ''
        }

        form = UserUpdateForm(data=data)
        self.assertFalse(form.is_valid())

    def test_valid_user_update_form(self):
        new_photo.image = SimpleUploadedFile(name='testimage.png', content=open(
            blog_app/tests/testdata/testimage.png, 'rb').read())

        form = UserUpdateForm(newPhoto.image)
        self.assertTrue(form.is_valid())

    def test_valid_user_update_form(self):
        data = {
            'image': ''
        }

        form = UserUpdateForm(data=data)
        self.assertFalse(form.is_valid())
