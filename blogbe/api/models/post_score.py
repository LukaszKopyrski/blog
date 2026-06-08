from django.db import models
from django.contrib.auth.models import AbstractUser
from api.models.user import CustomUser
from api.models.post import Post

class PostScore(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='post_scores')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='scores')
    date = models.DateTimeField(auto_now_add=True, null=False)