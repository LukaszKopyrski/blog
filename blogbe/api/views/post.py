from rest_framework import status
from rest_framework.views import APIView
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.response import Response
from api.models.post import CustomUser,Post
from api.models.post_score import PostScore
from api.serializers.post import PostSerializer,PostScoreSerializer
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from api.permissions import IsAuthorOrReadOnly, IsAuthorOrAdmin

class PostListCreateView(ListCreateAPIView):
    queryset = Post.objects.select_related("user")
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class PostDetailsView(RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.select_related("user")
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly,IsAuthorOrAdmin]
    http_method_names = ["get","patch", "delete"]



