from django.db import models
from userapp.models import CustomUser
from tagapp.models import Tag


class Post(models.Model):
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    content = models.CharField(max_length=2200)
    created_at = models.DateTimeField(auto_now_add=True)
    likes_count = models.IntegerField(default=0)
    comments_count = models.IntegerField(default=0)
    post_image = models.ImageField(upload_to='postpic', null=True, blank=True)
    tags = models.ManyToManyField(Tag)

    def __str__(self):
        return "Post by: " + self.author.username + " at " + str(self.created_at)





