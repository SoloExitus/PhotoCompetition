import django_filters
from django.db.models import Count
from django.views.generic.base import TemplateView
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from competition.models import PhotoPost, PhotoPostState
from competition.permissions import AuthorAllStaffChange
from competition.serializers import PhotoPostListSerializer, PhotoPostDetailSerializer


class HomePageView(TemplateView):
    template_name = "competition/base.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['pageTitle'] = 'Gallery'
        return context


class GalleryViewSet(viewsets.ReadOnlyModelViewSet):
    """
     provides `list` and `retrieve` actions.
    """
    queryset = PhotoPost.objects.filter(state=PhotoPostState.APPROVED).annotate(
            likes_count=Count('likes', distinct=True),
            comments_count=Count('comments', distinct=True),
    )

    def get_serializer_class(self):
        if self.action == 'list':
            return PhotoPostListSerializer
        elif self.action == 'retrieve':
            return PhotoPostDetailSerializer


class UserPostViewSet(viewsets.ModelViewSet):
    permission_classes = (AuthorAllStaffChange,)
    serializer_class = PhotoPostListSerializer

    def get_queryset(self):
        user = self.request.user
        return PhotoPost.objects.filter(user=user).annotate(
            likes_count=Count('likes', distinct=True),
            comments_count=Count('comments', distinct=True),
        )

