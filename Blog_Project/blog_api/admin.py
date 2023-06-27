from django.contrib import admin
from blog_api.models import Post, Comment, Category, Like, SubComment, UserProfile
# Register your models here.

admin.site.register(Post)
admin.site.register(UserProfile)
admin.site.register(Comment)
admin.site.register(Category)
admin.site.register(Like)
admin.site.register(SubComment)