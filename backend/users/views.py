from api.pagination import PageNumberLimitPagination
from api.viewsets import ListModelViewSet, SwitchOnOffViewSet
from rest_framework import permissions

from .models import User
from .serializers import SubscribedUserSerializer


class SubscriptionsViewSet(ListModelViewSet):
    serializer_class = SubscribedUserSerializer
    permission_classes = (permissions.IsAuthenticated,)
    pagination_class = PageNumberLimitPagination

    def get_queryset(self):
        return self.request.user.follower.all()


class SubscribeViewSet(SwitchOnOffViewSet):
    model_class = User
    serializer_class = SubscribedUserSerializer
    router_pk = "user_id"
    error_text_create = "Подписка уже существует"
    error_text_destroy = "Подписки не существует"

    def is_on(self) -> bool:
        user = self.get_object()

        return self.request.user.follower.filter(id=user.id).exists()

    def create(self, request, *args, **kwargs):
        user = self.get_object()

        if self.request.user.id == user.id:
            return self.error("Невозможно подписаться на самого себя")

        return super().create(request, *args, **kwargs)

    def perform_create(self, serializer: SubscribedUserSerializer):
        user = self.get_object()

        self.request.user.follower.add(user)
        self.request.user.save()

    def perform_destroy(self, instance: User):
        self.request.user.follower.remove(instance)
        self.request.user.save()
