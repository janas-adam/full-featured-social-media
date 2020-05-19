import os
from django.test import TestCase
from users.forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from django.contrib.auth.models import User
from django.test.client import Client
from django.urls import reverse
from django.http import HttpResponse
from django.core.files.uploadedfile import SimpleUploadedFile


class BlogTestCase(TestCase):

    client = Client()

    def setUp(self):
        self.client = Client()
        self.credentials = {
            'username': 'testuser',
            'password': 'testpassword'
        }
        self.client.user = User.objects.create_user(**self.credentials)
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

    def test_valid_user_update_form(self):
        self.client.login(username='testuser', password='testpassword')

        data = {
            'username': 'testuser2',
            'email': 'testemail2@test.com'
        }

        form = UserUpdateForm(data=data)
        self.assertTrue(form.is_valid())

    def test_valid_user_update_form(self):
        self.client.login(username='testuser', password='testpassword')

        data = {
            'username': 'testuser2',
            'email': ''
        }

        form = UserUpdateForm(data=data)
        self.assertFalse(form.is_valid())

    def test_valid_user_update_form(self):
        self.client.login(username='testuser', password='testpassword')

        new_photo.image = SimpleUploadedFile(name='testimage.png', content=open(
            users/tests/testdata/testimage.png, 'rb').read())

        form = UserUpdateForm(newPhoto.image)
        self.assertTrue(form.is_valid())

    def test_valid_user_update_form(self):
        self.client.login(username='testuser', password='testpassword')

        data = {
            'image': ''
        }

        form = UserUpdateForm(data=data)
        self.assertFalse(form.is_valid())
