from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from .serializers import CommentSerializer, CommentUpdateSerializer, CommentCreateSerializer
from .models import Comment
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_403_FORBIDDEN, HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND, HTTP_201_CREATED
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.shortcuts import get_object_or_404
from postapp.models import Post
class CommentsOfPostApiView(APIView):
    permission_classes = [AllowAny, ]

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('post_id', openapi.IN_PATH, description="ID of the post", type=openapi.TYPE_INTEGER),
        ],
        responses={
            200: openapi.Response('Successful response', CommentSerializer(many=True)),
            404: openapi.Response('There are no comments under this post!'),
        },
        operation_summary="Get comments of a post",
    )

    def get(self, request, post_id):
        comments = Comment.objects.filter(post_id=post_id)
        if comments.exists() == False:
            return Response({"message": "There are no comments under this post!"}, status=HTTP_404_NOT_FOUND)
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data, status=HTTP_200_OK)

class CommentApiView(APIView):
    permission_classes = [IsAuthenticated,]

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('comment_id', openapi.IN_PATH, description="ID of the comment",
                              type=openapi.TYPE_INTEGER),
        ],
        responses={
            200: openapi.Response('Successful response', CommentSerializer()),
            404: openapi.Response('This comment does not exist!'),
        },
        operation_summary="Get a comment by its id",
    )

    def get(self, request, comment_id):
        try:
            comment = Comment.objects.get(id=comment_id)
            data = CommentSerializer(comment, many=False).data
            return Response(data, status=HTTP_200_OK)
        except Comment.DoesNotExist:
            return Response({"message": "This comment does not exist!"}, status=HTTP_404_NOT_FOUND)

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('comment_id', openapi.IN_PATH, description="ID of the comment",
                              type=openapi.TYPE_INTEGER),
        ],
        request_body=CommentUpdateSerializer(),
        responses={
            200: openapi.Response('Successful response', CommentSerializer()),
            400: openapi.Response('Bad request, invalid data provided'),
            403: openapi.Response('Forbidden, you are not author of the comment!'),
            404: openapi.Response('Not found, this comment does not exist!'),
        },
        operation_summary="Update your comment by its id",
    )

    def patch(self, request, comment_id):
        try:
            comment = Comment.objects.get(id=comment_id)
            if request.user == comment.author:
                serializer = CommentUpdateSerializer(comment, data=request.data, partial=True)
                if serializer.is_valid():
                    serializer.save()
                    data = CommentSerializer(comment, many=False).data
                    return Response(data, status=HTTP_200_OK)
                return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
            return Response({'message': 'You are not author of the comment!'}, status=HTTP_403_FORBIDDEN)
        except Comment.DoesNotExist:
            return Response({"message": "This comment does not exist!"}, status=HTTP_404_NOT_FOUND)

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('comment_id', openapi.IN_PATH, description="ID of the comment",
                              type=openapi.TYPE_INTEGER),
        ],
        responses={
            200: openapi.Response('Comment is deleted'),
            403: openapi.Response('Forbidden, unable to delete the comment'),
            404: openapi.Response('Not found, this comment does not exist!'),
        },
        operation_summary="Delete your comment or a comment on your post by its ID",
    )

    def delete(self, request, comment_id):
        try:
            comment = Comment.objects.get(id=comment_id)
            post = comment.post
            if request.user == comment.author or request.user == post.author:
                comment.delete()
                post.comments_count -=1
                return Response({'message': 'Comment is deleted'}, status=HTTP_200_OK)
            return Response({'message': 'You cannot delete this comment because either you are not the author or this comment does not belong to your post.'}, status=HTTP_403_FORBIDDEN)
        except Comment.DoesNotExist:
            return Response({"message": "This comment does not exist!"}, status=HTTP_404_NOT_FOUND)


class CommentCreateApiView(APIView):
    permission_classes = [IsAuthenticated, ]

    @swagger_auto_schema(
        request_body=CommentCreateSerializer,
        responses={
            HTTP_201_CREATED: openapi.Response('Comment created', CommentSerializer),
            HTTP_400_BAD_REQUEST: openapi.Response('Bad request'),
        },
        operation_summary="Create a new comment",
    )
    def post(self, request, post_id):
        serializer = CommentCreateSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            post = get_object_or_404(Post, pk=post_id)
            post.comments_count+=1
            post.save()
            serializer.save(author=request.user, post=post)
            comment = CommentSerializer(serializer.instance).data
            return Response(comment, status=HTTP_201_CREATED)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)




