from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_201_CREATED, HTTP_200_OK, HTTP_403_FORBIDDEN, HTTP_404_NOT_FOUND
from .models import UserFollowing
from userapp.models import CustomUser
from userapp.serializers import FollowedUserSerializer
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
class FollowUserApiView(APIView):
    permission_classes = [IsAuthenticated, ]
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'followed_user_id': openapi.Schema(type=openapi.TYPE_INTEGER),
            },
            required=['followed_user_id'],
        ),
        responses={
            201: openapi.Response('You followed a user', schema=openapi.Schema(type=openapi.TYPE_OBJECT)),
            400: openapi.Response('Bad request, invalid data provided',
                                  schema=openapi.Schema(type=openapi.TYPE_OBJECT)),
            404: openapi.Response('Not found, This user does not exist!', schema=openapi.Schema(type=openapi.TYPE_OBJECT)),
        },
        operation_summary="Follow a user",
    )

    def post(self, request):
        try:
            followed_user_id = request.data.get('followed_user_id')

            if not followed_user_id:
                return Response({'message': 'Please provide followed_user_id.'},
                                status=HTTP_400_BAD_REQUEST)

            followed_user = CustomUser.objects.get(id=followed_user_id)
            if request.user == followed_user:
                return Response({'message': 'You cannot follow yourself.'}, status=HTTP_400_BAD_REQUEST)

            if UserFollowing.objects.filter(follower=request.user, followed_user=followed_user).exists():
                return Response({'message': 'You are already following this user.'}, status=HTTP_400_BAD_REQUEST)

            follow_instance = UserFollowing.objects.create(follower=request.user, followed_user=followed_user)
            request.user.following_count += 1
            request.user.save()

            followed_user.followers_count += 1
            followed_user.save()
            return Response({'message': f'You followed {followed_user.username}'}, status=HTTP_201_CREATED)
        except CustomUser.DoesNotExist:
            return Response({'message': 'This user does not exist!'}, status=HTTP_404_NOT_FOUND)

class UnfollowUserApiView(APIView):
    permission_classes = [IsAuthenticated,]
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'followed_user_id': openapi.Schema(type=openapi.TYPE_INTEGER),
            },
            required=['followed_user_id'],
        ),
        responses={
            200: openapi.Response('You unfollowed a user', schema=openapi.Schema(type=openapi.TYPE_OBJECT)),
            400: openapi.Response('Bad request, invalid data provided',
                                  schema=openapi.Schema(type=openapi.TYPE_OBJECT)),
            403: openapi.Response('Forbidden, unable to unfollow the user',
                                  schema=openapi.Schema(type=openapi.TYPE_OBJECT)),
            404: openapi.Response('Not found, this user does not exists', schema=openapi.Schema(type=openapi.TYPE_OBJECT)),
        },
        operation_summary="Unfollow a user",
    )

    def post(self, request):
        try:
            followed_user_id = request.data.get('followed_user_id')

            if not followed_user_id:
                return Response({'message': 'Please provide followed_user_id.'}, status=HTTP_400_BAD_REQUEST)

            followed_user = CustomUser.objects.get(id=followed_user_id)

            if request.user == followed_user:
                return Response({'message': 'You cannot unfollow yourself.'}, status=HTTP_400_BAD_REQUEST)

            user_following = UserFollowing.objects.filter(follower=request.user, followed_user=followed_user)

            if user_following.exists():
                user_following.delete()

                request.user.following_count -= 1
                request.user.save()

                followed_user.followers_count -= 1
                followed_user.save()

                return Response({'message': f'You unfollowed {followed_user.username}'}, status=HTTP_200_OK)

            return Response({'message': f'You cannot unfollow {followed_user.username} because you did not even follow them.'}, status=HTTP_403_FORBIDDEN)
        except CustomUser.DoesNotExist:
            return Response({'message': 'This user does not exist!'}, status=HTTP_404_NOT_FOUND)

class FollowingListApiView(APIView):
    permission_classes = [IsAuthenticated, ]

    @swagger_auto_schema(
        responses={
            200: openapi.Response('Successful response', FollowedUserSerializer()),
        },
        operation_summary="Get a list of users followed by the current user",
    )
    def get(self, request):
        following_users = UserFollowing.objects.filter(follower=request.user).values_list('followed_user', flat=True)
        following_users_objects = CustomUser.objects.filter(id__in=following_users)
        serializer = FollowedUserSerializer(following_users_objects, many=True)
        return Response(serializer.data, status=HTTP_200_OK)

class FollowersListApiView(APIView):
    @swagger_auto_schema(
        responses={
            200: openapi.Response('Successful response', FollowedUserSerializer()),
        },
        operation_summary="Get a list of the current user's followers",
    )
    def get(self, request):
        followers = UserFollowing.objects.filter(followed_user=request.user).values_list('follower', flat=True)
        followers_objects = CustomUser.objects.filter(id__in=followers)
        serializer = FollowedUserSerializer(followers_objects, many=True)
        return Response(serializer.data, status=HTTP_200_OK)




