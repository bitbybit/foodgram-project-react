from django.urls import include, path
from rest_framework.routers import SimpleRouter

from .views import TagViewSet

router = SimpleRouter()
router.register("tags", TagViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
