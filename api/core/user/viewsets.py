from rest_framework import viewsets
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated, AllowAny

from django.http import Http404

from core.user.models import User
from core.user.serializers import UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    http_method_names = ("patch", "get", "delete")
    serializer_class = UserSerializer

    def get_permissions(self):
        if self.action == "retrieve":
            return [AllowAny()]
        return [IsAuthenticated()]

    def get_queryset(self):
        user = self.request.user

        if not user.is_authenticated:
            return User.objects.none()

        if user.is_superuser:
            return User.objects.all()

        return User.objects.filter(public_id=user.public_id)

    def get_object(self):
        try:
            obj = User.objects.get_object_by_public_id(self.kwargs["pk"])
        except Http404 as e:
            raise Http404("User not found.") from e

        user = self.request.user
        if not user.is_superuser and obj != user:
            raise PermissionDenied("You don't have permission to access this user.")

        self.check_object_permissions(self.request, obj)
        return obj