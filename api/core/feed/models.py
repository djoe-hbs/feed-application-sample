import uuid

from django.db import models

from core.user.models import User


class Feed(models.Model):
    public_id = models.UUIDField(default=uuid.uuid4, db_index=True, unique=True, editable=False)

    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="feeds")
    title = models.CharField(max_length=255)
    content = models.TextField(max_length=3000)

    created = models.DateTimeField(auto_now=True)
    updated = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.author.username} - {self.title}"
    