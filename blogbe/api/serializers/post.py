from rest_framework import serializers
import re
from api.models.post import Post
from api.serializers.post_score import PostScoreSerializer
from api.serializers.comment import CommentSerializer

class PostSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField(source='get_username', read_only=True)
    comments = serializers.SerializerMethodField(source='get_comments', read_only=True)
    score = serializers.SerializerMethodField(source='get_score')
    scores = serializers.SerializerMethodField(source='get_scores')
    date = serializers.DateTimeField(format="%Y/%m/%d %H:%M", read_only=True)
    is_author = serializers.SerializerMethodField(read_only=True)
    is_staff = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Post
        fields = ['id', 'title', 'topic', 'score', 'scores', 'content', 'date', 'username', 'comments','is_author','is_staff']

    def validate_title(self, value):
        regex = r'^[\w\s!?,.\:/-]{2,32}$'
        if not re.match(regex, value):
            raise serializers.ValidationError("Title may contain only letters, numbers spaces and special characters: ! ? , . : / -. It must be between 2 and 32 characters.")
        return value

    def validate_topic(self, value):
        regex = r'^[\w\s!?,.\:/-]{2,32}$'
        if not re.match(regex, value):
            raise serializers.ValidationError("Topic may contain only letters, numbers spaces and special characters: ! ? , . : / -. It must be between 2 and 32 characters.")
        return value

    def validate_content(self, value):
        regex = r'^[\w\s!?,.\:/-]{2,512}$'
        if not re.match(regex, value):
            raise serializers.ValidationError("Content may contain only letters, numbers spaces and special characters: ! ? , . : / -. It must be between 2 and 512 characters.")
        return value    

    def get_username(self, obj):
        return obj.user.username

    def get_score(self, obj):
        return len(obj.scores.all())
    
    def get_scores(self, obj):
        scores = obj.scores.all()
        score_serializer = PostScoreSerializer(scores, many=True)
        return score_serializer.data

    def get_comments(self, obj):
        comments = obj.comments.all()
        comment_serializer = CommentSerializer(comments, many=True, context=self.context)
        return comment_serializer.data

    def get_is_author(self, obj):
        request = self.context.get('request', None)
        if request and request.user.is_authenticated:
            return obj.user == request.user
        return False
    
    def get_is_staff(self, obj):
        request = self.context.get('request', None)
        if request and request.user.is_authenticated:
            return request.user.is_staff
        return False

