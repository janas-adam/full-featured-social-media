from django.contrib import admin
from .models import Post, Category, MenuOption, Comment, PostLike, CommentLike

admin.site.register(Post)
admin.site.register(Category)
admin.site.register(MenuOption)
admin.site.register(Comment)
admin.site.register(PostLike)
admin.site.register(CommentLike)