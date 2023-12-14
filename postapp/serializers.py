from rest_framework.serializers import ModelSerializer, SerializerMethodField
from rest_framework import serializers
from .models import Post
from tagapp.serializers import TagSerializer, TagCreateSerializer
from tagapp.models import Tag

class PostSerializer(ModelSerializer):
    author_username = SerializerMethodField()
    tags = TagSerializer(many=True, read_only=True)
    class Meta:
        model = Post
        fields = ['author', 'author_username','content', 'created_at', 'likes_count', 'comments_count', 'post_image', 'tags', ]
        read_only_fields = ['author_username', 'tags']
    def get_author_username(self, obj):
        return obj.author.username if obj.author else None

class PostCreateSerializer(ModelSerializer):
    post_image = serializers.ImageField(max_length=None, use_url=True)
    tags = TagCreateSerializer(many=True, required=False)
    class Meta:
        model = Post
        fields = ['content', 'post_image', 'tags']

    # tags always null ;(
    def create(self, validated_data):
        tags_data = validated_data.pop('tags', [])
        post = Post.objects.create(**validated_data)

        for tag_data in tags_data:
            tag_serializer = TagCreateSerializer(data=tag_data)
            if tag_serializer.is_valid():
                tag = tag_serializer.save()
                post.tags.add(tag)
        return post

class PostUpdateSerializer(ModelSerializer):
    class Meta:
        model = Post
        fields = ['content']
