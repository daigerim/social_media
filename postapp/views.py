from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND
from userapp.models import CustomUser
from .serializers import *
import requests
import phpserialize
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from rest_framework.parsers import MultiPartParser

class AllPostsApiView(APIView):
    permission_classes = [AllowAny, ]

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(name='order_by', in_=openapi.IN_QUERY, type=openapi.TYPE_STRING, required=False,
                              description='Specify the field by which posts should be ordered.'),
            openapi.Parameter(name='author', in_=openapi.IN_QUERY, type=openapi.TYPE_STRING, required=False,
                              description='Filter posts by author username'),
            openapi.Parameter(name='tags', in_=openapi.IN_QUERY, type=openapi.TYPE_STRING, required=False,
                              description='Filter posts by tag name'),
            openapi.Parameter(name='search', in_=openapi.IN_QUERY, type=openapi.TYPE_STRING, required=False,
                              description='Search posts by city'),
        ],
        responses={
            200: PostSerializer(many=True)
        },
        operation_summary="Getting all the post or posts by filter/search"
    )

    def get(self, request):
        posts = Post.objects.all()

        if 'order_by' in request.GET.keys():
            ordering = request.GET.get('order_by')
            posts = posts.order_by(ordering)

        if 'author' in request.GET.keys():
            author_username = request.GET.get('author')
            posts = posts.filter(author__username=author_username)

        if 'tags' in request.GET.keys():
            tag_names = request.GET.getlist('tags')
            posts = posts.filter(tags__tag_name__in=tag_names)

        if 'search' in request.GET.keys():
            search = request.GET.get('search')
            posts = posts.filter(location_city__icontains=search)

        serializer = PostSerializer(posts, many=True)
        data = serializer.data
        return Response(data, status=HTTP_200_OK)

class PostDetailView(APIView):
    permission_classes = [AllowAny, ]
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('id', openapi.IN_PATH, description="ID of the comment",
                              type=openapi.TYPE_INTEGER),
        ],
        responses={
            200: openapi.Response('Successful response', PostSerializer()),
            404: openapi.Response('Not found, this post does not exist!'),
        },
        operation_summary="Get a post by its id",
    )
    def get(self, request, pk):
        try:
            post = Post.objects.get(id=pk)
        except Post.DoesNotExist:
            return Response({"error": "This post does not exist!"}, status=HTTP_404_NOT_FOUND)
        serializer = PostSerializer(post)
        return Response(serializer.data, status=HTTP_200_OK)

class PostCreateApiView(APIView):
    permission_classes = [IsAuthenticated, ]
    parser_classes = [MultiPartParser, ]

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(name='content', in_=openapi.IN_FORM, type=openapi.TYPE_STRING, required=True),
            openapi.Parameter(name='post_image', in_=openapi.IN_FORM, type=openapi.TYPE_FILE, required=True),
            openapi.Parameter(name='tags', in_=openapi.IN_FORM, type=openapi.TYPE_INTEGER, required=True),
        ],
        responses={
            200: openapi.Response('Post is created!', PostSerializer()),
            400: openapi.Response('Bad request'),
        },
        operation_summary="Create a new post",
    )
    def post(self, request):
        serializer = PostCreateSerializer(data=request.data, partial=False)
        if serializer.is_valid():
            client_ip = self.get_client_ip(request)
            #client_ip = '91.231.66.169'
            #client_ip ='51.158.98.121'
            #client_ip='113.171.48.50'
            # For an example: 94.157.209.5
            location = self.get_location_from_ip(client_ip)

            author_id = request.user.id
            author_instance = CustomUser.objects.get(pk=author_id)

            serializer.validated_data['author'] = author_instance
            serializer.validated_data['location_city'] = location['city']
            serializer.validated_data['location_country'] = location['country']
            serializer.validated_data['longitude'] = location['longitude']
            serializer.validated_data['latitude'] = location['latitude']

            serializer.save()
            request.user.post_count +=1
            request.user.save()

            return Response(serializer.data, status=HTTP_200_OK)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip

    def get_location_from_ip(self, ip_address):
        base_url = f"http://www.geoplugin.net/json.gp?ip={ip_address}"

        try:
            response = requests.get(base_url)
            data = response.json()
            print(data)

            if 'geoplugin_city' not in data or 'geoplugin_countryName' not in data:
                return {'city': None, 'country': None, 'longitude': None, 'latitude': None}

            location = {
                'city': data.get('geoplugin_city'),
                'country': data.get('geoplugin_countryName'),
                'longitude': data.get('geoplugin_longitude'),
                'latitude': data.get('geoplugin_latitude'),
            }
            return location
        except requests.exceptions.RequestException as e:
            print(f"Error fetching location: {e}")
            return {'city': None, 'country': None, 'longitude': None, 'latitude': None}

class UserOwnPostApiView(APIView):
    permission_classes = [IsAuthenticated, ]

    @swagger_auto_schema(
        responses={
            200: openapi.Response('Successful response', PostSerializer()),
        },
        operation_summary="Get user's posts",
    )

    def get(self, request):
        user_posts = Post.objects.filter(author=request.user)
        serializer = PostSerializer(user_posts, many=True)
        return Response(serializer.data, status=HTTP_200_OK)

class UserOwnPostUpdateorDeleteApiView(APIView):
    permission_classes = [IsAuthenticated, ]
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('id', openapi.IN_PATH, description="ID of the post",
                              type=openapi.TYPE_INTEGER),
        ],
        request_body=PostUpdateSerializer(),
        responses={
            200: openapi.Response('Successful response', PostSerializer()),
            400: openapi.Response('Bad request, invalid data provided'),
            404: openapi.Response('Not found, this post does not exist!'),
        },
        operation_summary="Update your post by its id",
    )
    def patch(self, request, pk):
        try:
            post = Post.objects.get(pk=pk, author=request.user)
        except Post.DoesNotExist:
            return Response({"error": "This post does not exist!"}, status=HTTP_404_NOT_FOUND)

        serializer = PostUpdateSerializer(post, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            data = PostSerializer(post).data
            request.user.post_count-=1
            request.user.save()
            return Response(data, status=HTTP_200_OK)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('id', openapi.IN_PATH, description="ID of the post",
                              type=openapi.TYPE_INTEGER),
        ],
        responses={
            200: openapi.Response('Post is deleted'),
            404: openapi.Response('Not found, this post does not exist!'),
        },
        operation_summary="Delete your post",
    )

    def delete(self, request, pk):
        try:
            post = Post.objects.get(pk=pk, author=request.user)
        except Post.DoesNotExist:
            return Response({"error": "Post not found"}, status=HTTP_404_NOT_FOUND)

        post.delete()
        return Response({'message': 'Post is deleted!'}, status=HTTP_200_OK)

class PostNearPlacesApiView(APIView):
    @swagger_auto_schema(
        manual_parameters = [
            openapi.Parameter(name='post_id', in_=openapi.IN_PATH, type=openapi.TYPE_INTEGER, required=True, description='ID of the post to retrieve nearby places.')],
        responses={
            200: openapi.Response("Nearby places data"),
            404: openapi.Response("No places found nearby or post does not exist!"),
        },
        operation_summary="Get nearby places for a post",
    )

    def get(self, request, post_id):
        try:
            post = Post.objects.get(pk=post_id)
            latitude = post.latitude
            longitude = post.longitude
            base_url = f"http://www.geoplugin.net/extras/nearby.gp?lat={latitude}&long={longitude}&output=php"
            response = requests.get(base_url)
            data = phpserialize.loads(response.content, decode_strings=True, charset='gb18030')
            if data:
                return Response(data, status=HTTP_200_OK)
            else:
                return Response({'message': 'No places found nearby!'}, status=HTTP_404_NOT_FOUND)

        except Exception as e:
            return Response({'message': f'No places found nearby or post does not exist!'}, status=HTTP_404_NOT_FOUND)