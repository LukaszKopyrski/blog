from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from api.models.post import CustomUser,Post
from api.models.post_score import PostScore
from api.serializers.post import PostScoreSerializer
from rest_framework.permissions import IsAuthenticated

class AddPostScoreView(APIView):
    permission_classes = [IsAuthenticated]        
    def post(self, request,post_id):
        post = Post.objects.get(pk=post_id)

        user = request.user
        request.data['user'] =user.id

        
        if PostScore.objects.filter(user=user.id, post=post.id).exists():
            return Response({'error':'Tylko raz użytkownik może dodać ocenę wpisu'})
        else:    
            serializer = PostScoreSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save(user=user, post=post)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class DeletePostScoreView(APIView):
    permission_classes = [IsAuthenticated]
    def delete(self, request, post_id, username):
        post = Post.objects.get(pk=post_id)
        user = CustomUser.objects.get(username=username)
        try:
            post_score = PostScore.objects.get(user=user, post=post)
            post_score.delete()
            return Response({"message":"Ocena wpisu została usunięta"}, status=status.HTTP_204_NO_CONTENT)
        except PostScore.DoesNotExist:
            return Response({'error': 'Ocena wpisu nie została znaleziona.'}, status=status.HTTP_404_NOT_FOUND)