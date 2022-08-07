from django.urls import include, path
from rest_framework.routers import SimpleRouter

router = SimpleRouter()

urlpatterns = [
    path("auth/", include("djoser.urls.authtoken")),
    path("", include("djoser.urls")),
    path("", include(router.urls)),
]
