from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_403_FORBIDDEN, HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND

from postapp.models import Post
from postapp.serializers import PostSerializer

from django.contrib.auth import login, authenticate, logout

from .serializers import *

class AuthUserApiView(APIView):
    permission_classes = [AllowAny, ]
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        user = authenticate(email=email, password=password)

        if user is not None:
            login(request, user)
            data = {'message': 'Welcome!'}
            return Response(data, HTTP_200_OK)
        else:
            data = {'message': 'Username or/and Password is not valid!'}
            return Response(data, HTTP_403_FORBIDDEN)

class LogoutUserApiView(APIView):
    permission_classes = [IsAuthenticated, ]
    def post(self, request):
        logout(request)
        return Response({'message': 'User logged out successfully!'}, status=HTTP_200_OK)

class ProfileUserApiView(APIView):
    permission_classes = [IsAuthenticated, ]
    # get request
    def get(self, request):
        try:
            user = request.user
            profile_data = UserSerializer(user).data
            user_posts = Post.objects.filter(author=request.user)
            posts_serializer = PostSerializer(user_posts, many=True).data
            data = {
                "profile": profile_data,
                "posts": posts_serializer
            }
            return Response(data, status=HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=HTTP_400_BAD_REQUEST)

    # patch request
    def patch(self, request):
        user = request.user
        serializer = UserUpdateSerializer(user, request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            data = UserSerializer(user).data
            return Response(data, status=HTTP_200_OK)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
    # delete request
    def delete(self, request):
        user = request.user
        if 'reason' in request.data.keys():
            print(user.username, request.data['reason'])
        user.delete()
        return Response({'message': 'User is deleted!'}, status=HTTP_200_OK)

class RegistrationUserApiView(APIView):
    permission_classes = [AllowAny, ]
    def post(self, request):
        serializer = UserCreateSerializer(data=request.data, partial=False)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=HTTP_200_OK)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
# maybe should not return the password and say something like user is created!


class OtherUserProfileApiView(APIView):
    permission_classes = [AllowAny, ]

    def get(self, request):
        username = request.query_params.get('username')
        if not username:
            return Response({"error": "Please provide a username"}, status=HTTP_400_BAD_REQUEST)

        try:
            user = CustomUser.objects.get(username=username)
            profile_data = UserSerializer(user).data
            other_user_posts = Post.objects.filter(author=user)
            posts_serializer = PostSerializer(other_user_posts, many=True).data

            data = {
                "profile": profile_data,
                "posts": posts_serializer
            }
            return Response(data, status=HTTP_200_OK)
        except CustomUser.DoesNotExist:
            return Response({"error": "User does not exist"}, status=HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=HTTP_400_BAD_REQUEST)