from blog_app.models import MenuOption, Category
from django.urls import reverse
from django.shortcuts import get_object_or_404


def get_menu_query(request):
	menu_query = MenuOption.objects.filter(auth=False)
	if request.user.is_authenticated:
		menu_query = MenuOption.objects.filter(auth=True)

	context = [{"url": reverse(menu_item.url), "title": menu_item.title} for menu_item in menu_query]

	return {'context' : context}

def get_category_query(request):
	categories = Category.objects.all()

	return {'categories' : categories}