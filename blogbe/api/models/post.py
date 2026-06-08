from django.db import models
from django.contrib.auth.models import AbstractUser
from api.models.user import CustomUser

class Post(models.Model):
    title = models.CharField(max_length=64, null=False)
    topic = models.CharField(max_length=64, null=False)
    content = models.TextField(max_length=512, null=False)
    date = models.DateTimeField(auto_now_add=True, null=False)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='posts')

    def __str__(self):
        return self.title
    
    class Meta:
        db_table = "Post"
        ordering = ['-date']
