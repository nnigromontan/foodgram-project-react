"""Представления приложения users."""

from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets, generics
from rest_framework.decorators import action
from rest_framework.permissions import (
    AllowAny, IsAuthenticated
)
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import User, Subscription
from .serializers import (
    SubscriptionSerializer, SubscribeSerializer, CurrentUserSerializer
)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = CurrentUserSerializer
    permission_classes = [AllowAny, ]

    @action(
        detail=False,
        methods=['get'],
        permission_classes=(IsAuthenticated, )
    )
    def me(self, request):
        serializer = self.get_serializer(self.request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)


class SubscribeView(APIView):
    permission_classes = [IsAuthenticated, ]

    def get(self, request, pk):
        user = request.user
        data = {
            'author': pk,
            'user': user.id
        }
        serializer = SubscribeSerializer(data=data,
                                         context={'request': request})
        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request, pk):
        user = request.user
        author = get_object_or_404(User, pk=pk)
        Subscription.objects.filter(user=user, author=author).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class SubscriptionViewSet(generics.ListAPIView):
    permission_classes = [IsAuthenticated, ]
    serializer_class = SubscriptionSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({'request': self.request})
        return context

    def get_queryset(self):
        user = self.request.user
        return User.objects.filter(subscribed__user=user)
