from django.urls import path
from .views import *

urlpatterns = [
    path('all/', TagsApiView.as_view()),
    path('create/', TagCreateApiView.as_view()),
    path('delete/<int:pk>/', TagApiView.as_view()),
]