from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_201_CREATED, HTTP_200_OK, HTTP_404_NOT_FOUND
from rest_framework.generics import ListAPIView
from .models import *
from .serializers import *

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

class LikePostApiView(APIView):
    permission_classes = [IsAuthenticated, ]

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('id', openapi.IN_PATH, description="ID of the post to be liked",
                              type=openapi.TYPE_INTEGER),
        ],
        responses={
            201: openapi.Response('Post liked successfully'),
            400: openapi.Response('Bad request or already liked'),
            404: openapi.Response('Not found, this post does not exist!'),
        },
        operation_summary="Like a post by its ID",
    )
    def post(self, request, pk):
        try:
            post = Post.objects.get(id=pk)
        except Post.DoesNotExist:
            return Response({'message': 'This post does not exist!'}, status=HTTP_404_NOT_FOUND)

        user = request.user

        if PostLike.objects.filter(post=post, user=user).exists():
            return Response({'message': 'You have already liked this post.'}, status=HTTP_400_BAD_REQUEST)

        like = PostLike.objects.create(post=post, user=user)

        post.likes_count += 1
        post.save()
        return Response({'message': 'Post liked successfully.'}, status=HTTP_201_CREATED)

class UnlikePostApiView(APIView):
    permission_classes = [IsAuthenticated, ]

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('id', openapi.IN_PATH, description="ID of the post to be unliked",
                              type=openapi.TYPE_INTEGER),
        ],
        responses={
            200: openapi.Response('Post unliked successfully'),
            400: openapi.Response('Bad request or already liked'),
            404: openapi.Response('Not found, this post does not exist!'),
        },
        operation_summary="Unlike a post by its ID",
    )
    def post(self, request, pk):
        try:
            post = Post.objects.get(id=pk)
        except Post.DoesNotExist:
            return Response({'message': 'This post does not exist!'}, status=HTTP_404_NOT_FOUND)

        user = request.user

        try:
            like = PostLike.objects.get(post=post, user=user)
        except PostLike.DoesNotExist:
            return Response({'message': 'You have not liked this post.'}, status=HTTP_400_BAD_REQUEST)

        like.delete()

        post.likes_count -= 1
        post.save()
        return Response({'message': 'Post unliked successfully.'}, status=HTTP_200_OK)


class CommentLikeApiView(APIView):
    permission_classes = [IsAuthenticated, ]

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('id', openapi.IN_PATH, description="ID of the comment to be liked",
                              type=openapi.TYPE_INTEGER),
        ],
        responses={
            201: openapi.Response('Comment liked successfully'),
            400: openapi.Response('Bad request or already liked'),
            404: openapi.Response('Not found, this comment does not exist!'),
        },
        operation_summary="Like a comment by its ID",
    )

    def post(self, request, pk):
        try:
            comment = Comment.objects.get(id=pk)
        except Comment.DoesNotExist:
            return Response({'message': 'This comment does not exist!'}, status=HTTP_404_NOT_FOUND)

        user = request.user

        if CommentLike.objects.filter(comment=comment, user=user).exists():
            return Response({'message': 'You have already liked this comment.'}, status=HTTP_400_BAD_REQUEST)

        like = CommentLike.objects.create(comment=comment, user=user)

        comment.likes_count += 1
        comment.save()

        comment_data = {
            'text': comment.content,
            'author': comment.author.username,
        }
        return Response({'message': 'Comment liked successfully.', 'comment': comment_data}, status=HTTP_201_CREATED)

class CommentUnlikeApiView(APIView):
    permission_classes = [IsAuthenticated, ]

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('id', openapi.IN_PATH, description="ID of the comment to be unliked",
                              type=openapi.TYPE_INTEGER),
        ],
        responses={
            200: openapi.Response('Comment unliked successfully'),
            400: openapi.Response('Bad request or already liked'),
            404: openapi.Response('Not found, this comment does not exist!'),
        },
        operation_summary="Unlike a comment by its ID",
    )

    def post(self, request, pk):
        try:
            comment = Comment.objects.get(id=pk)
        except Comment.DoesNotExist:
            return Response({'message': 'This comment does not exist!'}, status=HTTP_404_NOT_FOUND)

        user = request.user

        try:
            like = CommentLike.objects.get(comment=comment, user=user)
        except CommentLike.DoesNotExist:
            return Response({'message': 'You have not liked this comment.'}, status=HTTP_400_BAD_REQUEST)

        like.delete()

        comment.likes_count -= 1
        comment.save()
        comment_data = {
            'text': comment.content,
            'author': comment.author.username,
        }
        return Response({'message': 'Comment unliked successfully.', 'comment': comment_data}, status=HTTP_200_OK)


class LikedPostsApiView(ListAPIView):
    @swagger_auto_schema(
        responses={
            200: openapi.Response('List of liked posts', schema=LikedPostSerializer(many=True)),
            404: openapi.Response('Not found, there are no liked posts', schema=openapi.Schema(type=openapi.TYPE_OBJECT)),
        },
        operation_summary="Get a list of user's liked posts",
    )
    def get(self, request):
        user = self.request.user
        liked_posts = PostLike.objects.filter(user=user).select_related('post')

        if not liked_posts.exists():
            return Response({"message": "There are no liked posts!"}, status=HTTP_404_NOT_FOUND)

        serializer = LikedPostSerializer(liked_posts, many=True)
        return Response(serializer.data, status=HTTP_200_OK)