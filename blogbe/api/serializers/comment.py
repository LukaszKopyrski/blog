from rest_framework import serializers
import re
from api.models.comment import Comment
from api.serializers.post_score import PostScoreSerializer
from api.serializers.reply import ReplySerializer

class CommentSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField(source='get_username', read_only=True)
    date = serializers.DateTimeField(format="%Y/%m/%d %H:%M", read_only=True)
    scores = serializers.SerializerMethodField(source='get_scores')
    score = serializers.SerializerMethodField(source='get_score')
    replies = serializers.SerializerMethodField(source='get_replies', read_only=True)
    is_author = serializers.SerializerMethodField(read_only=True)
    is_staff = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'username', 'score', 'scores', 'content', 'date', 'replies', 'is_author', 'is_staff']

    def validate_content(self, value):
        regex = r'^[\w\s!?,.\:/-]{2,256}$'
        if not re.match(regex, value):
            raise serializers.ValidationError("Treść może zawierać tylko litery, cyfry, spacje oraz dozwolone znaki specjalne: !?,.:/- o długości od 2 do 256 znaków")
        return value

    def get_username(self, obj):
        return obj.user.username
    
    def get_score(self, obj):
        return len(obj.scores.all())
    
    def get_scores(self, obj):
        scores = obj.scores.all()
        score_serializer = PostScoreSerializer(scores, many=True)
        return score_serializer.data

    def get_replies(self, obj):
        replies = obj.replies.all()
        reply_serializer = ReplySerializer(replies, many=True, context=self.context)
        return reply_serializer.data
    
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
