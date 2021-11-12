from rest_framework.routers import SimpleRouter

from competition.views import PhotoPostViewSet

router = SimpleRouter()

router.register(r'gallery', PhotoPostViewSet, basename='post')

urlpatterns = router.urls