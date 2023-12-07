from django.urls import path
from .views import *

urlpatterns = [
    path('auth/', AuthUserApiView.as_view()),
]