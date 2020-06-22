from django.contrib import admin

# Register your models here.
from blog.models import Post


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Post._meta.fields]