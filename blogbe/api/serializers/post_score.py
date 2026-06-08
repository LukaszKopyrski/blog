from rest_framework import serializers
from api.models.post_score import  PostScore


class PostScoreSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField(source='get_username', read_only=True)
    date = serializers.DateTimeField(format="%Y/%m/%d %H:%M", read_only=True)

    class Meta:
        model = PostScore
        fields = ['id', 'username', 'date']
    
    def get_username(self, obj):
        return obj.user.username
