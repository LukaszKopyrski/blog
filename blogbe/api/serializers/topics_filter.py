from rest_framework import serializers

class TopicsFilterSerializer(serializers.Serializer):
    topic = serializers.CharField(min_length=2, max_length=32)