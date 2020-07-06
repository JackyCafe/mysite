from django.contrib import admin

# Register your models here.
from blog.models import Post,Comment


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
     list_display = [field.name for field in Post._meta.fields]


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
     list_display = [field.name for field in Comment._meta.fields]
