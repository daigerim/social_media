from .models import UserFollowing
from rest_framework.serializers import ModelSerializer

class UserFollowingSerializer(ModelSerializer):
    class Meta:
        model = UserFollowing
        fields = ['id', 'follower', 'followed_user']
