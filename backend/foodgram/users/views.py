"""Представления приложения users."""

from djoser.views import UserViewSet
from django.shortcuts import get_list_or_404, get_object_or_404
from rest_framework import status, views, filters
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
                context={'request':request},
                many=True,
            )
            return self.get_paginated_response(serializer.data)
        return Response(serializer.data, status=status.HTTP_200_OK)


class SubscriptionViewSet(ListAPIView):
    serializer_class = SubscriptionSerializer
    pagination_class = CustomPagination
    filter_backends = (filters.SearchFilter, )
    permission_classes = (IsAuthenticated, )
    search_fields = ('^subscribed__user', )

    def get_queryset(self):
        user = self.request.user
        return User.objects.filter(subscriber__user=user)


class SubscribeView(views.APIView):
    pagination_class = CustomPagination
    permission_classes = (IsAuthenticated,)

    def post(self, request, pk):
        author = get_object_or_404(User, pk=pk)
        user = self.request.user
        data = {'author': author.id, 'user': user.id}
        serializer = SubscribeSerializer(
            data=data, context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(data=serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request, pk):
        author = get_object_or_404(User, pk=pk)
        user = self.request.user
        subscription = get_object_or_404(
            Subscription, user=user, author=author
        )
        subscription.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
