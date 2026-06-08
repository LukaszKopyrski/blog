from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from api.serializers.user import CustomUserSerializer

class MyAccountView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        serializer = CustomUserSerializer(user)
        return Response(serializer.data)

    def patch(self, request):
        user = request.user
        if user.is_demo:
            return Response({"error":"Demo accounts cannot bo modified"}, status=status.HTTP_403_FORBIDDEN)
        serializer = CustomUserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self,request):
        user = request.user
        if not user.is_demo:
            user.delete()
            response = Response({"message":"user deleted"}, status=status.HTTP_200_OK)
            response.delete_cookie("access_token")
            response.delete_cookie("refresh_token")
            return response
        else:
            return Response({"error":"Demo accounts cannot be deleted"})