from django.db import models
from userapp.models import CustomUser

class UserFollowing(models.Model):
    follower = models.ForeignKey(CustomUser,  related_name='follower_set', on_delete=models.CASCADE)
    followed_user = models.ForeignKey(CustomUser,  related_name='following_set', on_delete=models.CASCADE)

    def __str__(self):
        return self.follower.username + " follows " + self.followed_user.username