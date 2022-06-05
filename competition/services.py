from django.contrib.auth import get_user_model

from service_objects.services import Service

from competition.models import PhotoPost, Like, Comment, PhotoPostState
from competition.forms import UpdatePostForm


def updatepost(request, pk) -> bool:
    user = request.user
    post = PhotoPost.objects.get(pk=pk)

    if not post:
        return False

    if not user.id == post.user.id:
        return False

    old_image = post.full_image

    form = UpdatePostForm(request.POST, request.FILES, instance=post)
    if form.is_valid():
        new_post = form.save(commit=False)
        new_image = new_post.full_image

        if old_image != new_image:
            new_post.previous_image = old_image
            new_post.state = PhotoPostState.NEW

            post.comments.all().delete()
            post.likes.all().delete()

        post.save()
        return True

    return False


def is_liked_post(instance, user) -> bool:
    if not user.is_authenticated:
        return False

    likes = Like.objects.filter(post=instance, user=user)
    return likes.exists()


def destroy_comment(request, pk):
    user = request.user
    comment = Comment.objects.get(id=pk)

    if not comment:
        return False

    if not user.id == comment.user.id:
        return False

    if comment.comment_children.exists():
        return False

    comment.delete()
    return True


def update_comment(request, pk):
    user = request.user
    comment = Comment.objects.get(id=pk)

    if not comment:
        return False

    if not user.id == comment.user.id:
        return False

    if comment.comment_children.exists():
        return False

    text = request.data["text"]

    comment.text = text
    comment.save()
    return True

