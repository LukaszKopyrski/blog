from django.db import models
from api.models.comment import Comment
from api.models.user import CustomUser

class Reply(models.Model):
    content = models.TextField(max_length=512, null=False)
    date = models.DateTimeField(auto_now_add=True, null=False)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='replies')
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='replies')

    def __str__(self):
        return self.content
    
    class Meta:
        db_table = "Reply"
        ordering = ['-date']

