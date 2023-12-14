from django.urls import path
from .views import *

urlpatterns = [
    path('auth/', AuthUserApiView.as_view()),
    path('registration/', RegistrationUserApiView.as_view()),
    path('profile/', ProfileUserApiView.as_view()),
    path('logout/', LogoutUserApiView.as_view()),
    path('other_user_profile/', OtherUserProfileApiView.as_view()),

]