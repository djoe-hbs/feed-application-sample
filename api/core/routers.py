from rest_framework import routers

from core.user.viewsets import UserViewSet
from core.auth.viewsets import RegisterViewSet, LoginViewSet, RefreshViewSet
from core.feed.viewsets import FeedViewSet

router = routers.DefaultRouter()

router.register(r"user", UserViewSet, basename="user")

router.register(r"auth/register", RegisterViewSet, basename="auth-register")
router.register(r"auth/login", LoginViewSet, basename="auth-login")
router.register(r"auth/refresh", RefreshViewSet, basename="auth-refresh")

router.register(r"feed/feed", FeedViewSet, basename="feed-feed")

urlpatterns = [
    *router.urls,
]