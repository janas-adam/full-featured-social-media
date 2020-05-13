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
	add_comment_to_post,
	remove_comment,
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
	path('post/<int:pk>/comment/', views.add_comment_to_post, name='add-comment'),
	path('comment/<int:pk>/remove/', views.remove_comment, name='remove-comment'),
	path('post/<int:pk>/like/', views.like_post, name='like-post'),
	path('comment/<int:pk>/like/', views.like_comment, name='like-comment'),
	path('post/<int:pk>/unlike/', views.unlike_post, name='unlike-post'),
	path('comment/<int:pk>/unlike/', views.unlike_comment, name='unlike-comment'),
	path('<int:category>', views.CategoryPostListView.as_view(), name='category')

]
