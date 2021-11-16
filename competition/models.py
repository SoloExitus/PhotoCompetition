from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django_fsm import FSMField, transition
from imagekit.models import ProcessedImageField, ImageSpecField
from pilkit.processors import ResizeToFill


class User(AbstractUser):
    email = models.EmailField(unique=True)

    thumbnail = ProcessedImageField(
        upload_to='user_thumbnail/',
        default='user_thumbnail/default.jpg',
        processors=[ResizeToFill(100, 100)],
        format='JPEG',
        options={'quality': 100},
        verbose_name='Миниатура пользователя',
    )

    # profile_pictures = models.ImageField(
    #         null=True,
    #         blank=True,
    #         default='default.jpg',
    #         upload_to='profile_pictures',
    #         verbose_name='profile picture',
    #     )

    REQUIRED_FIELDS = ['email', 'password']

    def __str__(self) -> str:
        return self.username


# class UserProfile(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     email = models.EmailField()
#     avatar = models.ImageField(upload_to='avatars', default='avatars/default.jpg')
#
#     def __str__(self):
#         return f"Profile of user:{self.user.username}"


class PhotoPostState(object):
    NEW = 'new'
    APPROVED = 'approved'
    REJECTED = 'rejected'
    REMOVED = 'removed'

    CHOICES = (
        (NEW, NEW),
        (APPROVED, APPROVED),
        (REJECTED, REJECTED),
        (REMOVED, REMOVED),
    )


class PhotoPost(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='Автор', on_delete=models.CASCADE, related_name='posts')
    title = models.CharField(max_length=256, verbose_name='Название поста')
    description = models.TextField(verbose_name='Описание поста', blank=True)

    state = FSMField(
        default=PhotoPostState.NEW,
        verbose_name='Состояние поста',
        choices=PhotoPostState.CHOICES,
        #protected=True,
    )

    published_date = models.DateTimeField(verbose_name='Дата публикации', null=True)
    remove_date = models.DateTimeField(verbose_name='Дата удаления', null=True)

    full_image = models.ImageField(verbose_name='Полное изображение', upload_to='photo/')

    preview_image = ImageSpecField(
        source='full_image',
        processors=[ResizeToFill(400, 400)],
        format='JPEG',
        options={'quality': 100},
    )

    previous_image = models.ImageField(null=True, verbose_name='Предыдущее используемое изображение', upload_to='photo/')
    comments = GenericRelation('comment')

    def __str__(self):
        return self.title

    ########################################################
    # Post state Transitions

    @transition(field=state, source=PhotoPostState.NEW, target=PhotoPostState.APPROVED)
    def approve(self):
        ''' Publish post'''

    @transition(field=state, source=PhotoPostState.NEW, target=PhotoPostState.REJECTED)
    def reject(self):
        ''' Set post state reject '''

    @transition(field=state, source=PhotoPostState.REJECTED, target=PhotoPostState.NEW)
    def revision(self):
        '''  Revert to the new state '''

    @transition(field=state, source=PhotoPostState.APPROVED, target=PhotoPostState.REMOVED)
    def remove(self):
        '''  Set remove state '''

    @transition(field=state, source=PhotoPostState.REMOVED, target=PhotoPostState.APPROVED)
    def restore(self):
        '''  Restore state to APPROVED '''


class Comment(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name='Автор',
        on_delete=models.CASCADE,
        related_name='comments'
    )

    text = models.TextField(verbose_name='Текст комментария')
    created_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    parent = models.ForeignKey(
        'self',
        verbose_name='Родительский комментарий',
        blank=True,
        null=True,
        related_name='comment_children',
        on_delete=models.CASCADE
    )

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True)
    object_id = models.PositiveIntegerField(null=True)

    class Meta:
        ordering = ('created_date',)

    def __str__(self):
        return f"{self.id}"


class Like(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name='Автор',
        on_delete=models.CASCADE,
        related_name='likes'
    )

    post = models.ForeignKey(PhotoPost, verbose_name='Пост', on_delete=models.CASCADE, related_name='likes')

    class Meta:
        unique_together = ('user', 'post')

    def __str__(self):
        return f'user:{self.user.username} like post:{self.post.title}'