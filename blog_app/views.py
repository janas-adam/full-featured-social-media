from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Post, Category, MenuOption, Comment, PostLike, CommentLike
from django.contrib.auth.models import User
from .forms import CommentForm
from django.urls import reverse
from django.contrib import messages
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)

class TestFuncMixin(object):

    def test_func(self):  
        obj = self.get_object()
        if self.request.user == obj.author:
            return True
        return False


class PostListView(ListView):
    model = Post
    template_name = 'blog/home.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 3


class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content', 'category']
    template_name = 'blog/post_form.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(TestFuncMixin, LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content']
    template_name = 'blog/post_form.html'

    def form_valid(self, form):  # user logged in is the author of the post
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostDeleteView(TestFuncMixin, LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = 'blog/post_confirm_delete.html'
    success_url = '/'


def about(request):
    return render(request, 'blog/about.html')


class UserPostListView(ListView):
    model = Post
    template_name = 'blog/user_posts.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 3

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')

class CategoryPostListView(ListView):
	model = Post
	template_name='blog/post_list.html'
	context_object_name = 'posts'
	ordering = ['-date_posted']
	paginate_by = 3

	def get_queryset(self):
		category = get_object_or_404(Category, id=self.kwargs['category'] )
		return Post.objects.filter(category=category).order_by('-date_posted')

class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    fields = ['content']
    template_name = 'blog/comment_form.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.post = get_object_or_404(Post, pk=self.kwargs['pk'])
        return super().form_valid(form)


class CommentDeleteView(TestFuncMixin, LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Comment
    template_name = 'blog/comment_confirm_delete.html'

    def get_success_url(self):
        self.post = get_object_or_404(Post, pk=self.kwargs['id'] )
        return reverse('post-detail', kwargs={'pk' : self.post.pk})


def like_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if PostLike.objects.filter(user=request.user, post=post).exists():
        messages.error(request, 'this post is already liked')
    else:
        new_like = PostLike.objects.create(user=request.user, post=post)


    return redirect('post-detail', pk=post.pk)


def like_comment(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    if CommentLike.objects.filter(user=request.user, comment=comment).exists():
        messages.error(request, 'this comment is already liked')
    else:
        new_like = CommentLike.objects.create(
            user=request.user, comment=comment)

    return redirect('post-detail', pk=comment.post.pk)

def unlike_post(request, pk):
	post = get_object_or_404(Post, pk=pk)
	if PostLike.objects.filter(user=request.user, post=post).exists():
		PostLike.objects.filter(user=request.user, post=post).delete()
	else:
		messages.error(request, 'you didn\'t like this post yet')

	return redirect('post-detail', pk=post.pk)

def unlike_comment(request, pk):
	comment = get_object_or_404(Comment, pk=pk)
	if CommentLike.objects.filter(user=request.user, comment=comment).exists():
		CommentLike.objects.filter(user=request.user, comment=comment).delete()
	else:
		messages.error(request, 'you didn\'t like this comment yet')

	return redirect('post-detail', pk=comment.post.pk)

