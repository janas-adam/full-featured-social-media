from django.contrib import admin
from django.urls import path, include
from users import views as user_views
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
	path('register/', user_views.register, name='register'),
    path('profile/', user_views.profile, name='profile'),
]