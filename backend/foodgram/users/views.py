"""Представления приложения users."""

from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets, serializers
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from core.pagination import CustomPagination
from .models import User, Subscription
from .serializers import SubscriptionSerializer


class SubscriptionViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, ]
    http_method_names = ['get', 'post', 'delete', ]
    serializer_class = SubscriptionSerializer
    pagination_class = CustomPagination

    def get_queryset(self):
        user = self.request.user
        return User.objects.filter(subscribed__user=user)

    def create(self, request, *args, **kwargs):
        author = get_object_or_404(User, pk=self.kwargs.get('user_id'))
        if self.request.user == author:
            raise serializers.ValidationError(
                'Нельзя подписаться на самого себя!'
            )
        if Subscription.objects.filter(
            user=self.request.user, author=author
        ).exists():
            raise serializers.ValidationError(
                'Такая подписка уже существует!'
            )
        Subscription.objects.create(user=self.request.user, author=author)
        serializer = SubscriptionSerializer(
            author,
            context={'request': request},
        )
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request, *args, **kwargs):
        author = get_object_or_404(User, pk=self.kwargs.get('user_id'))
        if not Subscription.objects.filter(
            user=self.request.user, author=author
        ).exists():
            raise serializers.ValidationError(
                'Такой подписки не существует!'
            )
        subscription = get_object_or_404(
            Subscription, user=self.request.user, author=author)
        subscription.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
