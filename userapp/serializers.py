from rest_framework.serializers import ModelSerializer
from .models import CustomUser

class UserCreateSerializer(ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['email', 'username', 'password']
    def create(self, validated_data):
        user = CustomUser.objects.create(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user

class AfterCreateUserSerializer(ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['email', 'username']

class UserSerializer(ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'bio', 'profile_picture', 'data_joined', 'followers_count', 'following_count', 'post_count', 'is_staff', 'is_superuser']

class UserUpdateSerializer(ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['username', 'bio', 'profile_picture']

class FollowedUserSerializer(ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['username', 'profile_picture']
