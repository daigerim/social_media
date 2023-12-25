from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND

from .models import Tag
from .serializers import TagSerializer, TagCreateSerializer

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

class TagsApiView(APIView):
    permission_classes = [AllowAny, ]
    @swagger_auto_schema(
        responses={
            200: openapi.Response('Successful response', TagSerializer(many=True)),
        },
        operation_summary="Get a list of all tags"
    )
    def get(self, request):
        categories = Tag.objects.all()
        data = TagSerializer(categories, many=True).data
        return Response(data, status=HTTP_200_OK)

class TagCreateApiView(APIView):
    permission_classes = [IsAuthenticated, ]
    @swagger_auto_schema(
        request_body=TagCreateSerializer(),
        responses={
            201: openapi.Response('Tag created successfully', TagSerializer()),
            400: openapi.Response('Bad request, invalid data provided'),
        },
        operation_summary="Create a new tag",
    )
    def post(self, request):
        serializer = TagCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=HTTP_201_CREATED)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

class TagApiView(APIView):
    permission_classes = [IsAuthenticated, ]

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('id', openapi.IN_PATH, description="ID of the tag to be deleted",
                              type=openapi.TYPE_INTEGER),
        ],
        responses={
            200: openapi.Response('Tag is deleted'),
            404: openapi.Response('Not found, this tag does not exist!'),
        },
        operation_summary="Delete a tag by its ID",
    )
    def delete(self, request, pk):
        try:
            tag = Tag.objects.get(id=pk)
            tag.delete()
            return Response({'message': 'Tag is deleted!'}, status=HTTP_200_OK)
        except Tag.DoesNotExist:
            return Response({'message': 'This tag does not exist!'}, status=HTTP_404_NOT_FOUND)




