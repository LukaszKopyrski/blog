from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly,IsAuthenticated
from django.shortcuts import get_object_or_404

from api.models.post import Post
from api.models.comment import Comment
from api.serializers.comment import CommentSerializer
from api.permissions import IsAuthorOrAdmin

class CommentListCreateView(ListCreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        post_id = self.kwargs["post_id"]
        return Comment.objects.select_related("user","post").filter(post_id=post_id)
    
    def perform_create(self, serializer):
        post = get_object_or_404(Post, pk=self.kwargs["post_id"])
        serializer.save(user=self.request.user, post=post)

class CommentDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.select_related("user","post")
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly,IsAuthorOrAdmin]

