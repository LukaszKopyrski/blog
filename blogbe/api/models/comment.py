from django.db import models
from api.models.user import CustomUser
from api.models.post import Post

class Comment(models.Model):
    content = models.TextField(max_length=512, null=False)
    date = models.DateTimeField(auto_now_add=True, null=False)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='comments')

    def __str__(self):
        return self.content
    
    class Meta:
        db_table = "Comment"
        ordering = ['-date']
