from django.db import models
from api.models.user import CustomUser
from api.models.post import Post
from api.models.comment import Comment

class CommentScore(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='comment_scores')
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='scores')
    date = models.DateTimeField(auto_now_add=True, null=False)