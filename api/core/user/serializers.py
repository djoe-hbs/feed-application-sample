from rest_framework import serializers
from django.core.exceptions import ValidationError as DjangoValidationError

from core.user.models import User


class UserSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(source="public_id", read_only=True, format="hex")
    image = serializers.ImageField(allow_null=True, required=False)

    class Meta:
        model = User
        fields = [
            "id", "username", "email",
            "first_name", "last_name",
            "bio", "image",
            "is_active", "is_staff", "is_superuser",
            "created", "updated"
        ]
        read_only_fields = [
            "is_active", "is_staff", "is_superuser",
            "created", "updated"
        ]

    def validate_email(self, value):
        """Unique email validation (case-insensitive)."""
        if self.instance and self.instance.email == value:
            return value

        if User.objects.filter(email__iexact=value).exists():
            raise serializers.ValidationError("This email is already in use.")
        return value
    