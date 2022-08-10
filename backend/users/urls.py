from django.urls import include, path
from rest_framework.routers import SimpleRouter

from .views import SubscribeViewSet, SubscriptionsViewSet

router = SimpleRouter()
router.register(
    r"users/(?P<user_id>\d+)/subscribe",
    SubscribeViewSet,
    basename="subscribe",
)
router.register(
    "users/subscriptions",
    SubscriptionsViewSet,
    basename="subscriptions",
)

urlpatterns = [
    path("auth/", include("djoser.urls.authtoken")),
    path("", include(router.urls)),
    path("", include("djoser.urls")),
]
