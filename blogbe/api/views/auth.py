from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate, login, logout
from api.models.user import CustomUser
from api.services.jwt_cookies import JwtCookieService
from rest_framework_simplejwt.views import TokenRefreshView

cookies = JwtCookieService()

class LoginView(APIView):
    def post(self, request):  
        email = request.data.get('email')
        password = request.data.get('password')
        
        if not email or not password:
            return Response({"errror":"email and password are required"}, status=status.HTTP_400_BAD_REQUEST)
        user = authenticate(request, email=email, password=password)
        if user is None:
            return Response({"error":"Invald credentials"}, status=status.HTTP_401_UNAUTHORIZED)
        refresh = RefreshToken.for_user(user)
        access = str(refresh.access_token)
        resp = Response({"ok":True}, status=status.HTTP_200_OK)
        cookies.set_access(resp, access)
        cookies.set_refresh(resp, str(refresh))
        return resp



class RefreshTokenView(TokenRefreshView):

    def post(self, request, *args, **kwargs):
        cookie_refresh = cookies.get_refresh(request)
        if not cookie_refresh:
            return Response({"error": "refresh cookie missing"}, status=401)

        request.data["refresh"] = cookie_refresh

        response_token = super().post(request, *args, **kwargs)

        access = response_token.data.get("access")
        new_refresh = response_token.data.get("refresh")

        resp = Response({"ok": True}, status=200)
        cookies.set_access(resp, access)
        if new_refresh:
            cookies.set_refresh(resp, new_refresh)
        return resp


class LogoutView(APIView):
    def post(self, request):
        cookie_refresh = cookies.get_refresh(request)

        resp = Response(status=status.HTTP_204_NO_CONTENT)
        cookies.clear(resp)

        if cookie_refresh:
            try:
                RefreshToken(cookie_refresh).blacklist()
            except Exception:
                pass

        return resp


class ResetPasswordView(APIView):
    def patch(self, request):
        email = request.data.get('email')
        answer = request.data.get('answer')
        new_password = request.data.get('new_password')

        try:
            user = CustomUser.objects.get(email=email)
            if answer == user.answer:
                user.set_password(new_password)
                user.save()
                return Response({'message': 'Password updated'}, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Invalid answer'}, status=status.HTTP_400_BAD_REQUEST)
        except CustomUser.DoesNotExist:
            return Response({'error': 'User does not exist'}, status=status.HTTP_404_NOT_FOUND)
