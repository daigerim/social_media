from django.urls import path
from .views import *

urlpatterns = [
    path('post_like/<int:pk>/', LikePostApiView.as_view()),
    path('post_unlike/<int:pk>/', UnlikePostApiView.as_view()),
    path('comment_like/<int:pk>/', CommentLikeApiView.as_view()),
    path('comment_unlike/<int:pk>/', CommentUnlikeApiView.as_view()),
    path('liked_posts/', LikedPostsApiView.as_view()),
]