from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND
from userapp.models import CustomUser
from .serializers import *

class AllPostsApiView(APIView):
    permission_classes = [AllowAny, ]
    def get(self, request):
        posts = Post.objects.all()
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data, status=HTTP_200_OK)

class PostDetailView(APIView):
    permission_classes = [AllowAny, ]
    def get(self, request, pk):
        try:
            post = Post.objects.get(pk=pk)
        except Post.DoesNotExist:
            return Response({"error": "This post does not exist!"}, status=HTTP_404_NOT_FOUND)
        serializer = PostSerializer(post)
        return Response(serializer.data, status=HTTP_200_OK)

class PostCreateApiView(APIView):
    permission_classes = [IsAuthenticated, ]
    def post(self, request):
        serializer = PostCreateSerializer(data=request.data)
        if serializer.is_valid():
            author_id = request.user.id
            author_instance = CustomUser.objects.get(pk=author_id)

            serializer.validated_data['author'] = author_instance
            serializer.save()

            return Response(serializer.data, status=HTTP_200_OK)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

class UserOwnPostApiView(APIView):
    permission_classes = [IsAuthenticated, ]
    def get(self, request):
        user_posts = Post.objects.filter(author=request.user)
        serializer = PostSerializer(user_posts, many=True)
        return Response(serializer.data)

    def patch(self, request, pk):
        try:
            post = Post.objects.get(pk=pk, author=request.user)
        except Post.DoesNotExist:
            return Response({"error": "This post does not exist!"}, status=HTTP_404_NOT_FOUND)

        serializer = PostUpdateSerializer(post, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            data = PostSerializer(post).data
            return Response(data, status=HTTP_200_OK)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            post = Post.objects.get(pk=pk, author=request.user)
        except Post.DoesNotExist:
            return Response({"error": "Post not found"}, status=HTTP_404_NOT_FOUND)

        post.delete()
        return Response({'message': 'Post is deleted!'}, status=HTTP_200_OK)

