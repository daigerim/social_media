from django.urls import path
from .views import *

urlpatterns = [
    path('follow_user/', FollowUserApiView.as_view()),
    path('unfollow_user/', UnfollowUserApiView.as_view()),
    path('following_list/', FollowingListApiView.as_view()),
    path('followers_list/', FollowersListApiView.as_view()),
]