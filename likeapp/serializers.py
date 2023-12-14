from rest_framework.serializers import ModelSerializer
from .models import PostLike

class LikedPostSerializer(ModelSerializer):
    class Meta:
        model = PostLike
        fields = ['post',]