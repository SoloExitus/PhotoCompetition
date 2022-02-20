import django_filters
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.http import HttpResponseRedirect, JsonResponse
from django.views.generic.base import TemplateView
from rest_framework import viewsets, status
from rest_framework.decorators import action, api_view, renderer_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.reverse import reverse_lazy

from competition import services
from competition.forms import PostForm
from competition.models import PhotoPost, PhotoPostState, Like
from competition.permissions import AuthorAllStaffChange, AuthUserButNotAuthorOrStuffOrSuper
from competition.serializers import PhotoPostListSerializer, PhotoPostDetailSerializer, PhotoPostInfoSerializer
from competition.mixins import LikePostMixin


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


class PhotoPostCreateView(TemplateView):
    template_name = "competition/photopostcreate.html"
    permission_classes = [IsAuthenticated]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['pageTitle'] = 'Create Post'
        context['form'] = PostForm()
        return context