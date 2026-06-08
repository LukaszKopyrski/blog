from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404

from api.models.user import CustomUser
from api.models.post import Post
from api.models.reply import Reply
from api.models.reply_score import ReplyScore
from api.serializers.reply import ReplySerializer
from api.serializers.reply_score import ReplyScoreSerializer
from api.permissions import IsAuthorOrAdmin


class AddReplyScoreView(APIView):
    permission_classes = [IsAuthenticated]        
    def post(self, request, reply_id):
        reply = Reply.objects.get(pk=reply_id)
        user = request.user


        if ReplyScore.objects.filter(user=user, reply=reply).exists():
            return Response({'error': 'Tylko raz użytkownik może dodać ocenę odpowiedzi'}, status=status.HTTP_400_BAD_REQUEST)
        
        
        serializer = ReplyScoreSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=user, reply=reply)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    
class DeleteReplyScoreView(APIView):
    permission_classes = [IsAuthenticated]
    def delete(self, request, reply_id, username):
        reply = Reply.objects.get(pk=reply_id)
        user = CustomUser.objects.get(username=username)
        try:
            reply_score = ReplyScore.objects.get(user=user, reply=reply)
            reply_score.delete()
            return Response({"message":"Ocena odpowiedzi została usunięta"}, status=status.HTTP_204_NO_CONTENT)
        except ReplyScore.DoesNotExist:
            return Response({'error': 'Ocena odpowiedzi nie została znaleziona.'}, status=status.HTTP_404_NOT_FOUND) 