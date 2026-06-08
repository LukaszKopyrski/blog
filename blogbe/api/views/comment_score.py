from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404

from api.models.user import CustomUser
from api.models.comment import Comment
from api.models.comment_score import CommentScore
from api.serializers.comment_score import  CommentScoreSerializer

class AddCommentScoreView(APIView):
    permission_classes = [IsAuthenticated]        
    def post(self, request, comment_id):
        comment = Comment.objects.get(pk=comment_id)
        user = request.user


        if CommentScore.objects.filter(user=user, comment=comment).exists():
            return Response({'error': 'Tylko raz użytkownik może dodać ocenę komentarza'}, status=status.HTTP_400_BAD_REQUEST)
        
        
        serializer = CommentScoreSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=user, comment=comment)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    
class DeleteCommentScoreView(APIView):
    permission_classes = [IsAuthenticated]
    def delete(self, request, comment_id, username):
        comment = Comment.objects.get(pk=comment_id)
        user = CustomUser.objects.get(username=username)
        try:
            comment_score = CommentScore.objects.get(user=user, comment=comment)
            comment_score.delete()
            return Response({"message":"Ocena komentarza została usunięta"}, status=status.HTTP_204_NO_CONTENT)
        except CommentScore.DoesNotExist:
            return Response({'error': 'Ocena komentarza nie została znaleziona.'}, status=status.HTTP_404_NOT_FOUND) 