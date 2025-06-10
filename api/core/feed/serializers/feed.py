from rest_framework import serializers

from core.feed.models import Feed


class FeedSerializer(serializers.ModelSerializer):
    
    id = serializers.UUIDField(source='public_id', read_only=True, format='hex')
    author = serializers.UUIDField(source='author.public_id', read_only=True, format='hex')

    class Meta:
        model = Feed
        fields = ["id", "author", "title",
                  "content", "created", "updated"]
        