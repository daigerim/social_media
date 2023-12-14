from django.urls import path
from .views import *

urlpatterns = [
    path('all/', AllPostsApiView.as_view()),
    path('new_post/', PostCreateApiView.as_view()),
    path('user_posts/', UserOwnPostApiView.as_view()),
    path('user_posts/<int:pk>/', UserOwnPostApiView.as_view()),
    path('detail_view/<int:pk>/', PostDetailView.as_view()),
]