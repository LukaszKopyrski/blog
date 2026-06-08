from rest_framework.views import APIView
from api.serializers.user import CustomUserSerializer
from rest_framework.response import Response
from rest_framework import status

class RegisterView(APIView):
    def post(self, request):
        serializer = CustomUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(CustomUserSerializer(user).data, status=status.HTTP_201_CREATED)