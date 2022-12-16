"""Представления приложения users."""

from djoser.views import UserViewSet
from django.shortcuts import get_list_or_404, get_object_or_404
from rest_framework import status, views
from rest_framework.decorators import action
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from core.pagination import CustomPagination
from users.models import Subscription, User
from users.serializers import (SubscribeSerializer,
                               SubscriptionSerializer,
                               CurrentUserSerializer)


class CreateUserView(UserViewSet):
    pagination_class = CustomPagination
    serializer_class = CurrentUserSerializer

    def get_queryset(self):
        return User.objects.all()

    @action(
        detail=False,
        permission_classes=(IsAuthenticated, ),
        pagination_class=CustomPagination
    )
    def subscriptions(self, request):
        subscribers = get_list_or_404(
            User, subscribed__user=self.request.user
        )
        page = self.paginate_queryset(subscribers)
        if page is not None:
            serializer = SubscriptionSerializer(
                page,
                context={'request': request},
                many=True,
            )
            return self.get_paginated_response(serializer.data)
        return Response(serializer.data, status=status.HTTP_200_OK)


class SubscriptionViewSet(ListAPIView):
    serializer_class = SubscriptionSerializer
    pagination_class = CustomPagination
    permission_classes = (IsAuthenticated, )

 
    def get_queryset(self):
        return User.objects.filter(subscribed__user=self.request.user)


class SubscribeView(views.APIView):
    serializer_class = SubscribeSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination

    def post(self, request, *args, **kwargs):
        user_id = self.kwargs.get('user_id')
        if user_id == request.user.id:
            return Response(
                {'error': 'Нельзя подписаться на себя'},
                status=status.HTTP_400_BAD_REQUEST
            )
        if Subscription.objects.filter(
                user=request.user,
                author_id=user_id
        ).exists():
            return Response(
                {'error': 'Вы уже подписаны на пользователя'},
                status=status.HTTP_400_BAD_REQUEST
            )
        author = get_object_or_404(User, id=user_id)
        Subscription.objects.create(
            user=request.user,
            author_id=user_id
        )
        return Response(
            self.serializer_class(author, context={'request': request}).data,
            status=status.HTTP_201_CREATED
        )

    def delete(self, request, *args, **kwargs):
        user_id = self.kwargs.get('user_id')
        get_object_or_404(User, id=user_id)
        subscription = Subscription.objects.filter(
            user=request.user,
            author_id=user_id
        )
        if subscription:
            subscription.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(
            {'error': 'Вы не подписаны на пользователя'},
            status=status.HTTP_400_BAD_REQUEST
        )
