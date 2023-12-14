from rest_framework.serializers import ModelSerializer, SerializerMethodField
from .models import Tag
from rest_framework import serializers

class TagSerializer(ModelSerializer):
    class Meta:
        model = Tag
        fields = ['tag_name']

class TagCreateSerializer(ModelSerializer):
    class Meta:
        model = Tag
        fields = ['tag_name']

    def validate_tag_name(self, value):
        if Tag.objects.filter(tag_name=value).exists():
            raise serializers.ValidationError("Tag with this name already exists.")
        return value