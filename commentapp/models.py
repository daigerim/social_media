from django.db import models
from postapp.models import Post
from userapp.models import CustomUser
from likeapp.models import CommentLike

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(CommentLike)

    def __str__(self):
        return f"Comment by {self.author.username} on {self.post}"
