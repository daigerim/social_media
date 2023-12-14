from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_201_CREATED, HTTP_200_OK
from rest_framework.generics import ListAPIView
from .models import *
from .serializers import *

class LikePostApiView(APIView):
    permission_classes = [IsAuthenticated, ]
    def post(self, request, pk):
        try:
            post = Post.objects.get(id=pk)
        except Post.DoesNotExist:
            return Response({'message': 'This post does not exist!'}, status=HTTP_400_BAD_REQUEST)

        user = request.user

        if PostLike.objects.filter(post=post, user=user).exists():
            return Response({'message': 'You have already liked this post.'}, status=HTTP_400_BAD_REQUEST)

        like = PostLike.objects.create(post=post, user=user)

        post.likes_count += 1
        post.save()
        return Response({'message': 'Post liked successfully.'}, status=HTTP_201_CREATED)

class UnlikePostApiView(APIView):
    permission_classes = [IsAuthenticated, ]
    def post(self, request, pk):
        try:
            post = Post.objects.get(id=pk)
        except Post.DoesNotExist:
            return Response({'message': 'This post does not exist!'}, status=HTTP_400_BAD_REQUEST)

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
    def post(self, request, pk):
        try:
            comment = Comment.objects.get(id=pk)
        except Comment.DoesNotExist:
            return Response({'message': 'This comment does not exist!'}, status=HTTP_400_BAD_REQUEST)

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
    def post(self, request, pk):
        try:
            comment = Comment.objects.get(id=pk)
        except Comment.DoesNotExist:
            return Response({'message': 'This comment does not exist!'}, status=HTTP_400_BAD_REQUEST)

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
    permission_classes = [IsAuthenticated, ]
    serializer_class = LikedPostSerializer
    def get_queryset(self):
        user = self.request.user
        liked_posts = PostLike.objects.filter(user=user).select_related('post')
        return liked_posts
