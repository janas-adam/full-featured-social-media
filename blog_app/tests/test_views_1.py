import os
from django.test import TestCase
from blog_app.models import Post, Category, MenuOption, Comment, PostLike, CommentLike
from django.contrib.auth.models import User
from django.test.client import Client
from django.urls import reverse
from django.http import HttpResponse


class BlogTestCase(TestCase):

    def setUp(self):
        self.numbers_of_post = 3
        self.client = Client()
        self.credentials = {
            'username': 'testuser',
            'password': 'testpassword'
        }
        self.client.user = User.objects.create_user(**self.credentials)
        self.category = Category.objects.create(name='testcategory')
        for post_id in range(1, self.numbers_of_post + 1):
            Post.objects.create(title=f'title{post_id}', author=self.client.user,
                                content=f'content{post_id}', category=self.category)
        self.post_list = Post.objects.all()
        self.post_first = Post.objects.get(pk=1)
        self.comment = Comment.objects.create(
            post=self.post_first, author=self.client.user, content='somecontent')
        os.environ['RECAPTCHA_DISABLE'] = 'True'


    def test_post_list(self):
        self.client.login(username='testuser', password='testpassword')
        url = reverse('blog-home')

        response = self.client.get(url)
        for model in self.post_list:
            self.assertIn(model.title, response.content.decode())
            self.assertIn(model.content, response.content.decode())
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed('blog/home.html')

    def test_post_list_is_paginated(self):
        self.client.login(username='testuser', password='testpassword')
        url = reverse('blog-home')
        self.numbers_of_post = 20

        for post_id in range(1, self.numbers_of_post + 1):
            Post.objects.create(title=f'title{post_id}', author=self.client.user,
                                content=f'content{post_id}', category=self.category)

        response = self.client.get(url)

        self.assertTrue('is_paginated' in response.context)
        self.assertTrue(response.context['is_paginated'] == True)

    def test_post_create(self):
        self.client.login(username='testuser', password='testpassword')
        url = reverse('post-create')

        data = {
            'title': 'testtitle1',
            'author': self.client.user,
            'content': 'testcontent',
            'category': self.category

        }

        response = self.client.post(url, data=data, follow=True)

        self.assertTemplateUsed('blog/post_form.html')
        self.assertIn(data['title'], response.content.decode())
        self.assertIn(data['content'], response.content.decode())
        self.assertEqual(response.status_code, 200)

    def test_post_delete(self):
        self.client.login(username='testuser', password='testpassword')

        url = reverse('post-delete', args=(self.post_first.pk,))

        response = self.client.post(url, follow=True)

        self.assertTemplateUsed('blog/post_confirm_delete.html')
        self.assertEqual(response.status_code, 200)
        self.assertFalse(self.post_first in self.post_list)

    def test_post_update(self):
        self.client.login(username='testuser', password='testpassword')

        url = reverse('post-update', args=(self.post_first.pk,))

        data = {
            'title': 'titleafterupdate',
            'content': 'contentafterupdate'

        }

        response = self.client.post(url, data=data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed('blog/post_form.html')
        self.assertIn(data['title'], response.content.decode())
        self.assertIn(data['content'], response.content.decode())

    def test_user_posts(self):
        self.client.login(username='testuser', password='testpassword')

        posts = Post.objects.filter(author=self.client.user)

        url = reverse('user-posts', kwargs={'username': 'testuser'})

        response = self.client.get(url)

        self.assertTemplateUsed('blog/user_posts.html')
        for obj in posts:
            self.assertIn(obj.title, response.content.decode())
            self.assertIn(obj.content, response.content.decode())

    def test_useless_view_about(self):

        url = reverse('blog-about')

        response = self.client.get(url)

        self.assertTemplateUsed('blog/about.html')

    def test_add_comment(self):
        self.client.login(username='testuser', password='testpassword')

        url = reverse('add-comment', args=(self.post_first.pk,))

        data = {
            'author': self.client.user,
            'content': 'testcomment1'

        }

        response = self.client.post(url, data=data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(data['content'], response.content.decode())

    def tearDown(self):
        del os.environ['RECAPTCHA_DISABLE']

    def test_remove_comment(self):
        self.client.login(username='testuser', password='testpassword')

        url = reverse('remove-comment', kwargs={'id': self.post_first.pk, 'pk' : self.comment.pk})

        response = self.client.post(url, follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertFalse(self.comment.content in response.content.decode())

    def test_post_like(self):
        self.client.login(username='testuser', password='testpassword')

        url = reverse('like-post', args=(self.post_first.pk,))

        data = {
            'user': self.client.user
        }

        response = self.client.post(url, data=data, follow=True)
        self.assertEqual(PostLike.objects.count(), 1)
        self.assertEqual(response.status_code, 200)

    def test_comment_like(self):
        self.client.login(username='testuser', password='testpassword')

        url = reverse('like-comment', args=(self.comment.pk,))

        data = {
            'user': self.client.user
        }

        response = self.client.post(url, data=data, follow=True)

        self.assertEqual(CommentLike.objects.count(), 1)
        self.assertEqual(response.status_code, 200)

    def test_post_unlike(self):
        self.client.login(username='testuser', password='testpassword')

        post_like = PostLike.objects.create(
            user=self.client.user, post=self.post_first)

        url = reverse('unlike-post', args=(self.post_first.pk,))

        response = self.client.post(url, follow=True)

        self.assertEqual(PostLike.objects.count(), 0)
        self.assertEqual(response.status_code, 200)

    def test_comment_unlike(self):
        self.client.login(username='testuser', password='testpassword')

        comment_like = CommentLike.objects.create(
            user=self.client.user, comment=self.comment)

        url = reverse('unlike-comment', args=(self.comment.pk,))

        response = self.client.post(url, follow=True)

        self.assertEqual(CommentLike.objects.count(), 0)
        self.assertEqual(response.status_code, 200)

    def test_category_post_list_view(self):

        posts = Post.objects.filter(category=self.category)

        url = reverse('category', args=(self.category.pk,))

        response = self.client.get(url)

        self.assertTemplateUsed('blog/post_list.html')
        for obj in posts:
            self.assertIn(obj.title, response.content.decode())
            self.assertIn(obj.content, response.content.decode())
