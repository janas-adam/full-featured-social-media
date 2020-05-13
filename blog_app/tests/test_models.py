import os
from django.test import TestCase
from blog_app.models import Post, Category, MenuOption, Comment, PostLike, CommentLike
from users.forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from django.contrib.auth.models import User
from django.test.client import Client
from django.urls import reverse
from django.http import HttpResponse


class BlogTestCase(TestCase):

    def setUp(self):

        self.client = Client()
        self.credentials = {
            'username': 'testuser',
            'password': 'testpassword'
        }
        self.client.user = User.objects.create_user(**self.credentials)
        self.category = Category.objects.create(name='testcategory')
        self.post = Post.objects.create(title='title1', author=self.client.user,
                                        content='content1', category=self.category)
        self.comment = Comment.objects.create(
            post=self.post, author=self.client.user, content='somecontent')
        os.environ['RECAPTCHA_DISABLE'] = 'True'

    def create_post(self):
        return Post.objects.create(title='title1', author=self.client.user, content='content1', category=self.category)

    def create_category(self):
        return Category.objects.create(name='category1')

    def create_comment(self):
        return Comment.objects.create(post=self.post, author=self.client.user, content='content1')

    def create_post_like(self):
        return PostLike.objects.create(user=self.client.user, post=self.post)

    def create_comment_like(self):
        return CommentLike.objects.create(user=self.client.user, comment=self.comment)

    def create_menu_option(self):
        return MenuOption.objects.create(title='title1', url='url1')

    def test_post_creation(self):
        post = self.create_post()
        self.assertTrue(isinstance(post, Post))
        self.assertTrue(Post.objects.count(), 2)

    def test_category_creation(self):
        category = self.create_category()
        self.assertTrue(isinstance(category, Category))
        self.assertTrue(Category.objects.count(), 2)

    def test_comment_creation(self):
        comment = self.create_comment()
        self.assertTrue(isinstance(comment, Comment))
        self.assertTrue(Comment.objects.count(), 2)

    def test_post_like_creation(self):
        post_like = self.create_post_like()
        self.assertTrue(isinstance(post_like, PostLike))

    def test_comment_like_creation(self):
        comment_like = self.create_comment_like()
        self.assertTrue(isinstance(comment_like, CommentLike))

    def test_menu_option_creation(self):
        menu_option = self.create_menu_option()
        self.assertTrue(isinstance(menu_option, MenuOption))
