from django.urls import path
from rest_framework.routers import SimpleRouter

from competition.viewsets import GalleryViewSet, UserPostViewSet, CommentsViewSet

router = SimpleRouter()

router.register(r'gallery', GalleryViewSet, basename='gallery')
router.register(r'profile', UserPostViewSet, basename='profile')
router.register(r'comment', CommentsViewSet, basename='comment')

urlpatterns = []

urlpatterns += router.urls