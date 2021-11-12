from django.contrib import admin
from django.utils.safestring import mark_safe

from competition.models import User, PhotoPost, Comment, Like


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'get_thumbnail', 'username', 'email')

    def get_thumbnail(self, obj):
        return mark_safe(f'<img src={obj.thumbnail.url} with="100" height="100">')

    get_thumbnail.short_description = 'иниатюра аватара пользователя'


@admin.register(PhotoPost)
class PhotoPostAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'get_preview_image', 'description', 'state')
    list_display_links = ('id', 'title', 'get_preview_image', 'description')

    def get_preview_image(self, obj):
        return mark_safe(f'<img src={obj.preview_image.url} with="400" height="400">')

    search_fields = ('id', 'title', 'status', 'description', 'published_date')


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'text', 'created_date', 'parent')
    list_display_links = ('id', 'text', 'created_date', 'parent')
    search_fields = ('text', 'created_date')


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'post')
    list_display_links = ('id', 'user', 'post')
    search_fields = ('user', 'post')
