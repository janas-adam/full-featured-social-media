from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse



class Post(models.Model):
    title = models.CharField(max_length=50)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    category = models.ForeignKey('Category', on_delete=models.CASCADE, null=True)
    date_posted = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title

    def get_absolute_url(self):  # return to url after creating the post#
        return reverse('post-detail', kwargs={'pk': self.pk})

class Category(models.Model):
	name = models.CharField(max_length=20)

	class Meta:
		verbose_name = 'category'
		verbose_name_plural = 'categories'

	def __str__(self):
		return self.name

class MenuOption(models.Model):
    title = models.CharField(max_length=25)
    url = models.CharField(max_length=200)
    auth = models.BooleanField(default=False)

    def __str__(self):
        return "%s,%s" % (self.title, self.auth)


class Comment(models.Model):
    post = models.ForeignKey(
        'Post', on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return "%s - %s" % (self.author, self.content)

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})


class PostLike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey('Post', on_delete=models.CASCADE)
    created_date = models.DateTimeField(default=timezone.now)

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})


class CommentLike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.ForeignKey(
        'Comment', on_delete=models.CASCADE, related_name='comment_likes')
    created_date = models.DateTimeField(default=timezone.now)

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})
