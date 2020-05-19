from . import views
from django.urls import path
from .views import (
	PostListView,
	PostDetailView,
	PostCreateView,
	PostUpdateView,
	PostDeleteView,
	UserPostListView,
	CategoryPostListView,
	CommentCreateView,
	CommentDeleteView,
	like_post,
	like_comment,
	unlike_post,
	unlike_comment,


)

urlpatterns = [
	path('', PostListView.as_view(), name='blog-home'),
	path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
	path('post/new/', PostCreateView.as_view(), name='post-create'),
	path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
	path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),
	path('user/<str:username>', UserPostListView.as_view(), name='user-posts'),
	path('about', views.about, name='blog-about'),
	path('post/<int:pk>/comment/', CommentCreateView.as_view(), name='add-comment'),
	path('post/<int:id>/comment/<int:pk>/remove/', CommentDeleteView.as_view(), name='remove-comment'),
	path('post/<int:pk>/like/', views.like_post, name='like-post'),
	path('comment/<int:pk>/like/', views.like_comment, name='like-comment'),
	path('post/<int:pk>/unlike/', views.unlike_post, name='unlike-post'),
	path('comment/<int:pk>/unlike/', views.unlike_comment, name='unlike-comment'),
	path('<int:category>', views.CategoryPostListView.as_view(), name='category')

]
