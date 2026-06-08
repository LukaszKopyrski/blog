from django.db import models
from api.models.comment import Comment
from api.models.user import CustomUser
from api.models.reply import Reply

class ReplyScore(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='reply_scores')
    reply = models.ForeignKey(Reply, on_delete=models.CASCADE, related_name='scores')
    date = models.DateTimeField(auto_now_add=True, null=False)