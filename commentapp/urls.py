from django.urls import path
from .views import *

urlpatterns = [
    path('post_comments/<int:post_id>', CommentsOfPostApiView.as_view()),
    path('comment_detail/<int:comment_id>/', CommentApiView.as_view()),
    path('new_comment/<int:post_id>/', CommentCreateApiView.as_view()),

]