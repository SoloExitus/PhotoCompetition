from django.contrib.auth import get_user_model
from service_objects.services import Service
from competition.models import PhotoPost, Like, Comment


def editpost(request, pk):
    user = request.user
    post = PhotoPost.objects.get(id=pk)

    if not post:
        return False

    if not user.id == post.user.id:
        return False

    print(request.data)
    title = request.data["text"]
    description = request.data["description"]
    full_image = request.data["full_image"]

    post.title = title
    post.description = description

    post.full_image = full_image

    post.save()
    return True


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

