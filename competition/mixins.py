from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from competition import services
from competition.permissions import AuthUserButNotAuthorOrStuffOrSuper
from competition.serializers import PhotoPostInfoSerializer, PostCommentSerializer


class LikePostMixin:
    @action(detail=True, methods=['post'], permission_classes=[AuthUserButNotAuthorOrStuffOrSuper])
    def like(self, request, pk=None):
        post = self.get_object()
        services.like_post(post, request.user)
        # post.refresh_from_db()
        serializer = PhotoPostInfoSerializer(post, context={'request': request})
        return Response(serializer.data)

    @action(detail=True, methods=['post'], permission_classes=[AuthUserButNotAuthorOrStuffOrSuper])
    def unlike(self, request, pk=None):
        post = self.get_object()
        services.unlike_post(post, request.user)
        # post.refresh_from_db()
        serializer = PhotoPostInfoSerializer(post, context={'request': request})
        return Response(serializer.data)
