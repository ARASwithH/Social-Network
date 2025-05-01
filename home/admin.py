from django.contrib import admin

from home.models import Post, Comment


# Register your models here.

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'auther')
    search_fields = ('title', 'slug')
    prepopulated_fields = {'slug': ('title',)}




@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('author', 'post', 'content')
    raw_id_fields = ('author', 'post')
