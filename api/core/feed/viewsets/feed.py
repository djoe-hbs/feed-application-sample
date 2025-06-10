from django.http import Http404

from rest_framework import viewsets
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from core.feed.models import Feed
from core.feed.serializers import FeedSerializer
from core.feed.permissions import IsOwnerOrSuperUser


class FeedViewSet(viewsets.ModelViewSet):
    serializer_class = FeedSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, IsOwnerOrSuperUser)
    http_method_names = ['get', 'post', 'patch', 'delete']

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return Feed.objects.all().order_by("-created")
        return Feed.objects.filter(author=user).order_by("-created")
    
    def get_object(self):
        try:
            obj = Feed.objects.get(public_id=self.kwargs["pk"])
        except Feed.DoesNotExist:
            raise Http404("Feed not found.")
        
        user = self.request.user
        if obj.author != user and not user.is_superuser:
            raise PermissionDenied("You do not have permission to access this feed.")
        
        self.check_object_permissions(self.request, obj)
        return obj
    
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
    
    def perform_update(self, serializer):
        serializer.save(author=self.request.user)