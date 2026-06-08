from rest_framework import serializers
from api.models.comment_score import  CommentScore

class CommentScoreSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField(source='get_username', read_only=True)
    date = serializers.DateTimeField(format="%Y/%m/%d %H:%M", read_only=True)

    class Meta:
        model = CommentScore
        fields = ['id', 'username', 'date']
    
    def get_username(self, obj):
        return obj.user.username