from django.db.models import Count
from django.views.generic.base import TemplateView
from rest_framework import viewsets
from competition.models import PhotoPost, PhotoPostState
from competition.serializers import PhotoPostListSerializer


class HomePageView(TemplateView):
    template_name = "competition/base.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['pageTitle'] = 'Gallery'
        return context


class PhotoPostViewSet(viewsets.ReadOnlyModelViewSet):
    """
     provides `list` and `retrieve` actions.
    """
    serializer_class = PhotoPostListSerializer


    def get_queryset(self):
        posts = PhotoPost.objects.filter(state=PhotoPostState.APPROVED).annotate(
            likes_count=Count('likes', distinct=True),
            comments_count=Count('comments', distinct=True),
            )
        return posts

    # def get_serializer_class(self):
    #     if (self.action == 'list'):
    #         return PhotoPostListSerializer
    #     elif (self.action == 'retrieve'):
    #         return PhotoPostDetailSerializer
