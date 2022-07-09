from django.contrib import admin
from django.utils.safestring import mark_safe

from competition.models import User, PhotoPost, Comment, Like


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'get_image', 'first_name', 'email')

    def get_image(self, obj):
        return mark_safe(f'<img src={obj.profile_image} with="100" height="100">')

    get_image.short_description = 'user profile image'


@admin.register(PhotoPost)
class PhotoPostAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'get_preview_image', 'description', 'state', 'approve_button')
    list_display_links = ('id', 'title', 'get_preview_image', 'description')

    def get_preview_image(self, obj):
        return mark_safe(f'<img src={obj.preview_image.url} with="400" height="400">')

    search_fields = ('id', 'title', 'status', 'description', 'published_at')

    def approve_button(self, obj):
        return mark_safe(f'<a class="button" >Кнопка</a>')


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'text', 'created_at', 'parent')
    list_display_links = ('id', 'user', 'text', 'created_at', 'parent')
    search_fields = ('user', 'text', 'created_at')


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'post')
    list_display_links = ('id', 'user', 'post')
    search_fields = ('user', 'post')


# #Отменить регистрацию предоставленного администратора модели
# admin.site.unregister(User)
#
# #Зарегистрируйте собственного администратора модели на основе UserAdmin по умолчанию
# @admin.register(User)
# class CustomUserAdmin(UserAdmin):
#     pass
