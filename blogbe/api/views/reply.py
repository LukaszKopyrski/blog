from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly,IsAuthenticated
from django.shortcuts import get_object_or_404

from api.models.user import CustomUser
from api.models.post import Post
from api.models.comment import Comment
from api.models.reply import Reply
from api.models.reply_score import ReplyScore
from api.serializers.reply import ReplySerializer, ReplyScoreSerializer
from api.permissions import IsAuthorOrAdmin

class ReplyListCreateView(ListCreateAPIView):
    serializer_class = ReplySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        comment_id = self.kwargs["comment_id"]
        return Reply.objects.select_related("user","comment").filter(comment_id=comment_id)
    
    def perform_create(self, serializer):
        comment = get_object_or_404(Comment, pk=self.kwargs["comment_id"])
        serializer.save(user=self.request.user, comment=comment)

class ReplyDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Reply.objects.select_related("user","comment")
    serializer_class = ReplySerializer
    permission_classes = [IsAuthenticatedOrReadOnly,IsAuthorOrAdmin]


