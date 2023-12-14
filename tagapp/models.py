from django.db import models

class Tag(models.Model):
    tag_name = models.CharField(max_length=50, null=True)
    def __str__(self):
        return self.tag_name
