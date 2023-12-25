from rest_framework.serializers import ModelSerializer, SerializerMethodField
from rest_framework import serializers
from .models import Post
from tagapp.serializers import TagSerializer
from tagapp.models import Tag

class PostSerializer(ModelSerializer):
    author_username = SerializerMethodField()
    tags = TagSerializer(many=True, read_only=True)
    class Meta:
        model = Post
        fields = ['id','author', 'author_username','content', 'created_at', 'likes_count', 'comments_count', 'post_image', 'tags', 'location_city', 'location_country']
        read_only_fields = ['author_username', 'tags']
    def get_author_username(self, obj):
        return obj.author.username if obj.author else None

class PostCreateSerializer(ModelSerializer):
    post_image = serializers.ImageField(max_length=None, use_url=True)
    class Meta:
        model = Post
        fields = ['content', 'post_image', 'tags','location_city', 'location_country', 'longitude', 'latitude']


class PostUpdateSerializer(ModelSerializer):
    class Meta:
        model = Post
        fields = ['content', 'tags']
