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


class PostListView(ListView):
    model = Post
    template_name = 'blog/home.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 3


class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = self.get_object()
        post_likes = PostLike.objects.filter(post=post).count()
        
       	context['post_likes'] = post_likes
       
        return context


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content', 'category']
    template_name = 'blog/post_form.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content']
    template_name = 'blog/post_form.html'

    def form_valid(self, form):  # user logged in is the author of the post#
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):  # it prevents users to update other people posts
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = 'blog/post_confirm_delete.html'
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


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
		self.category = get_object_or_404(Category, id=self.kwargs['category'] )
		return Post.objects.filter(category=self.category).order_by('-date_posted')


def add_comment_to_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.post = post
            comment.save()
            return redirect('post-detail', pk=post.pk)
    else:
        form = CommentForm()
    return render(request, 'blog/comment_form.html', {'form': form})

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


def remove_comment(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.delete()
    return redirect('post-detail', pk=comment.post.pk)


def like_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if PostLike.objects.filter(user=request.user, post=post).exists():
        messages.error(request, 'this post is already liked')
    else:
        new_like = PostLike.objects.create(user=request.user, post=post)
        new_like.save()

    return redirect('post-detail', pk=post.pk)


def like_comment(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    if CommentLike.objects.filter(user=request.user, comment=comment).exists():
        messages.error(request, 'this comment is already liked')
    else:
        new_like = CommentLike.objects.create(
            user=request.user, comment=comment)
        new_like.save()

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


