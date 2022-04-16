from rest_framework import viewsets, status
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import generics

from competition.models import PhotoPost, Comment, PhotoPostState
from competition.permissions import AuthorAllStaffChange, IsAuthorCommentChange
from competition.serializers import PhotoPostListSerializer, PhotoPostDetailSerializer, CommentsSerializer
from competition.mixins import LikePostMixin
from competition.services import destroy_comment, update_comment


class GalleryViewSet(LikePostMixin, viewsets.ReadOnlyModelViewSet):
    """
     provides default `list` and `retrieve` actions and like/unlike actions.
    """
    queryset = PhotoPost.objects.filter(state=PhotoPostState.APPROVED)

    def get_serializer_class(self):
        if self.action == 'list':
            return PhotoPostListSerializer
        elif self.action == 'retrieve':
            return PhotoPostDetailSerializer


class UserPostViewSet(viewsets.ModelViewSet):
    permission_classes = [AuthorAllStaffChange]
    serializer_class = PhotoPostListSerializer

    def get_queryset(self):
        user = self.request.user
        return PhotoPost.objects.filter(user=user)

    def create(self, request, *args, **kwargs):
        #import pdb

        #pdb.set_trace()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class CommentsViewSet(viewsets.mixins.CreateModelMixin, viewsets.mixins.UpdateModelMixin,
                      viewsets.mixins.DestroyModelMixin, viewsets.GenericViewSet):
    permission_classes = [IsAuthorCommentChange]
    serializer_class = CommentsSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def destroy(self, request, *args, **kwargs):
        do = destroy_comment(request, kwargs['pk'])
        if do:
            return Response(status=status.HTTP_202_ACCEPTED)
        return Response(status=status.HTTP_403_FORBIDDEN)

    def update(self, request, *args, **kwargs):
        do = update_comment(request, kwargs['pk'])
        if do:
            return Response(status=status.HTTP_202_ACCEPTED)
        return Response(status=status.HTTP_403_FORBIDDEN)

