from rest_framework import serializers
import re
from api.models.reply import Reply
from api.serializers.reply_score import ReplyScoreSerializer

class ReplySerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField(source='get_username', read_only=True)
    date = serializers.DateTimeField(format="%Y/%m/%d %H:%M", read_only=True)
    scores = serializers.SerializerMethodField(source='get_scores')
    score = serializers.SerializerMethodField(source='get_score')
    is_author = serializers.SerializerMethodField(read_only=True)
    is_staff = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Reply
        fields = ['id', 'username', 'score', 'scores', 'content', 'date', 'is_author', 'is_staff']

    def validate_content(self, value):
        regex = r'^[\w\s!?,.\:/-]{2,256}$'
        if not re.match(regex, value):
            raise serializers.ValidationError("Content may contain only letters, numbers spaces and special characters: ! ? , . : / -. It must be between 2 and 256 characters.")
        return value

    def get_username(self, obj):
        return obj.user.username

    def get_score(self, obj):
        return len(obj.scores.all())
    
    def get_scores(self, obj):
        scores = obj.scores.all()
        score_serializer = ReplyScoreSerializer(scores, many=True)
        return score_serializer.data

    def get_is_author(self, obj):
        request = self.context.get('request', None)
        user = getattr(request, 'user', None)
        if user and user.is_authenticated:
            return obj.user == user
        return False
    
    def get_is_staff(self, obj):
        request = self.context.get('request', None)
        user = getattr(request, 'user', None)
        if user and user.is_authenticated:
            return user.is_staff
        return False
    
