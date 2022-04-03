from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django_fsm import FSMField, transition
from imagekit.models import ProcessedImageField, ImageSpecField
from pilkit.processors import ResizeToFill


class User(AbstractUser):
    email = models.EmailField(unique=True)

    profile_image = models.CharField(max_length=256, default="/static/placeholders/avatar.jpg")

    REQUIRED_FIELDS = ['email', 'password']

    def __str__(self) -> str:
        return self.username


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
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name='Author',
        on_delete=models.CASCADE,
        related_name='posts'
    )

    title = models.CharField(max_length=256)
    description = models.TextField(blank=True)

    state = FSMField(
        default=PhotoPostState.NEW,
        choices=PhotoPostState.CHOICES,
    )

    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Create date')
    published_at = models.DateTimeField(auto_now_add=True, verbose_name='Publish date')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Last update date')

    full_image = models.ImageField(verbose_name='Full image', upload_to='photo/')

    preview_image = ImageSpecField(
        source='full_image',
        processors=[ResizeToFill(400, 400)],
        format='JPEG',
        options={'quality': 100},
    )

    previous_image = models.ImageField(
        upload_to='photo/',
        default='placeholders/postImage.png',
        verbose_name='Previous image'
    )

    @property
    def total_likes(self):
        return self.likes.count()

    @property
    def total_comments(self):
        return self.comments.count()

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
        verbose_name='Author',
        on_delete=models.CASCADE,
        related_name='comments'
    )

    post = models.ForeignKey(PhotoPost, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Create date')

    parent = models.ForeignKey(
        'self',
        verbose_name='Parent comment',
        blank=True,
        null=True,
        related_name='comment_children',
        on_delete=models.CASCADE
    )

    class Meta:
        ordering = ('created_at',)

    def __str__(self):
        return f'Comment by {self.user}'


class Like(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name='Author',
        on_delete=models.CASCADE,
        related_name='likes'
    )

    post = models.ForeignKey(PhotoPost, on_delete=models.CASCADE, related_name='likes')

    class Meta:
        unique_together = ('user', 'post')

    def __str__(self):
        return f'user:{self.user.username} like post:{self.post.title}'