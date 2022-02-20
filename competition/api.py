from django.urls import path
from rest_framework.routers import SimpleRouter

from competition.views import GalleryViewSet, UserPostViewSet

router = SimpleRouter()

router.register(r'gallery', GalleryViewSet, basename='gallery')
router.register(r'profile', UserPostViewSet, basename='profile')

urlpatterns =[
]

urlpatterns += router.urls