from rest_framework.serializers import ModelSerializer, SerializerMethodField
from .models import Comment

class CommentSerializer(ModelSerializer):
    author_username = SerializerMethodField()
    class Meta:
        model = Comment
        fields = ['post', 'author', 'author_username', 'content', 'created_at', 'likes_count']
        read_only_field =['author_username']
    def get_author_username(self, obj):
        return obj.author.username if obj.author else None

class CommentUpdateSerializer(ModelSerializer):
    class Meta:
        model = Comment
        fields = ['content']


class CommentCreateSerializer(ModelSerializer):
    class Meta:
        model = Comment
        fields = ['content']
