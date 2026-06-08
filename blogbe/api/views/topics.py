from rest_framework.views import APIView
from rest_framework.response import Response
from api.models.post import Post
from api.serializers.post import PostSerializer
from api.serializers.topics_filter import TopicsFilterSerializer

class AllTopicsView(APIView):
    def get(self, request, *args, **kwargs):
        topics = Post.objects.values_list("topic",flat=True).distinct()
        return Response([{"topic":t} for t in topics])
    
class TopicsFilterView(APIView):
    def get(self, request, topic):
        serializer = TopicsFilterSerializer(data={"topic":topic})
        serializer.is_valid(raise_exception=True)

        topic_value = serializer.validated_data["topic"]

        queryset = Post.objects.filter(topic__iexact=topic_value)
        serializer = PostSerializer(queryset, many=True, context={"request":request})
        return Response(serializer.data)