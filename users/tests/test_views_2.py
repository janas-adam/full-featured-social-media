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

    def test_create_user(self):
        url = reverse('register')

        data = {
            'username': 'testuser1',
            'email': 'testemail1@test.com',
            'password1': 'testpassword1',
            'password2': 'testpassword1',

        }

        response = self.client.post(url, data=data, format='json', follow=True)

        self.assertEqual(User.objects.count(), 2)
        self.assertEqual(response.status_code, 200)

    def test_login(self):
        response = self.client.post(
            reverse('login'), self.credentials, follow=True)
        self.assertTrue(response.context['user'].is_authenticated)

    def test_update_profile(self):
        self.client.login(username='testuser', password='testpassword')

        url = reverse('profile')

        data = {
            'username': 'testuser2',
            'email': 'testemail2@test.com'

        }

        response = self.client.post(url, data=data, format='json', follow=True)

        self.client.user.refresh_from_db()

        self.assertEqual(data['username'], self.client.user.username)
        self.assertEqual(data['email'], self.client.user.email)
        self.assertEqual(response.status_code, 200)