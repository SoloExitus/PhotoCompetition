import django_filters
from django import forms
from django.db.models import Count
from django.views.generic import CreateView, UpdateView
from django.views.generic.base import TemplateView
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.reverse import reverse_lazy

from competition.forms import PostForm
from competition.models import PhotoPost, PhotoPostState
from competition.permissions import AuthorAllStaffChange
from competition.serializers import PhotoPostListSerializer, PhotoPostDetailSerializer


class HomePageView(TemplateView):
    template_name = "competition/gallery.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['pageTitle'] = 'Competition Gallery'
        return context


class PostDetailView(TemplateView):
    template_name = "competition/post_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['pageTitle'] = 'Competition Post'
        return context


class ProfileView(TemplateView):
    template_name = "competition/profile.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['pageTitle'] = 'Competition Profile'
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

    def perform_create(self, serializer):
        kwargs = {
            'user': self.request.user,
            'author': self.request.user
        }

        serializer.save(**kwargs)

    def create(self, request, *args, **kwargs):
        #request.data['author'] = self.request.user
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class PhotoPostCreateView(CreateView):

    model = PhotoPost
    success_url = reverse_lazy('profile-list')
    fields = ['title', 'description', 'full_image']
    template_name = 'competition/photopostcreate.html'



# class PhotoPostCreateView(TemplateView):
#     template_name = "competition/photopostcreate.html"
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['pageTitle'] = 'Create Post'
#         context['form'] = PostForm()
#         return context