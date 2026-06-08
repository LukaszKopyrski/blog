from rest_framework import serializers
from api.models.reply_score import ReplyScore


class ReplyScoreSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField(source='get_username', read_only=True)
    date = serializers.DateTimeField(format="%Y/%m/%d %H:%M", read_only=True)

    class Meta:
        model = ReplyScore
        fields = ['id', 'username', 'date']
    
    def get_username(self, obj):
        return obj.user.username