"""Представления приложения users."""

from django.shortcuts import get_object_or_404
from rest_framework import status, views, filters
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from core.pagination import CustomPagination
from users.models import Subscription, User
from .serializers import SubscribeSerializer, SubscriptionSerializer


class SubscriptionViewSet(ListAPIView):
    serializer_class = SubscriptionSerializer
    pagination_class = CustomPagination
    permission_classes = (IsAuthenticated,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('^subscribed__user',)

    def get_queryset(self):
        user = self.request.user
        return User.objects.filter(subscribed__user=user)


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
