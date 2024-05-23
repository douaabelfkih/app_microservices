from django.shortcuts import redirect, render
from rest_framework import generics ,status , permissions , serializers
from django.contrib.auth.models import User
from .serializers import RegistrationSerializer, UserSerializer
from rest_framework.response import Response
import uuid
from django.contrib.sessions.models import Session
import jwt
from django.conf import settings
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from rest_framework.views import APIView
from django.core.cache import cache
from rest_framework_simplejwt.tokens import RefreshToken

def generate_access_token(user):
    payload = {
        'user_id': user.id,
        'username': user.username,
        # Ajoutez d'autres données pertinentes à votre access token si nécessaire
    }
    return jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')


from django.shortcuts import redirect

class RegistrationAPIView(generics.GenericAPIView):

    serializer_class = RegistrationSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        access_token = generate_access_token(user)
        request.session['access_token'] = access_token

        if serializer.is_valid():
            serializer.save()
            # Redirection explicite vers la page d'accueil du microservice de produits
            return HttpResponseRedirect('/auth/users/')
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




class DetailUser(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get(self, request, *args, **kwargs):
        # Vérifier la présence et la validité du token d'accès dans la session
        access_token = request.session.get('access_token')
        if access_token:
            try:
                # Vérifier la validité du token
                payload = jwt.decode(access_token, settings.SECRET_KEY, algorithms=['HS256'])
                # Si le token est valide, autoriser l'accès au service des produits
                return super().get(request, *args, **kwargs)
            except jwt.exceptions.InvalidTokenError:
                # Si le token est invalide, renvoyer une erreur d'authentification
                return Response({'error': 'Invalid access token'}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            # Si le token n'est pas présent, renvoyer une erreur d'authentification
            return Response({'error': 'No access token found'}, status=status.HTTP_401_UNAUTHORIZED)

def getusers(request):
    users = User.objects.all()
    return HttpResponse(users)


def getuser(request,pk):
    user = User.objects.get(pk=pk)
    return JsonResponse({'username':user.username})


class LoginView(generics.GenericAPIView):
    permission_classes = (AllowAny,)
    serializer_class = UserSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        refresh = RefreshToken.for_user(user)
        
        # Handle cart migration
        session_id = self.request.session.session_key
        if session_id:
            # Call the cart service to migrate the cart
            headers = {
                'Authorization': f'Bearer {str(refresh.access_token)}',
                'Content-Type': 'application/json'
            }
            cart_migration_url = 'http://20.199.21.250:8002/api/cart/migrate/'
            try:
                requests.post(cart_migration_url, headers=headers, json={'session_id': session_id})
            except requests.exceptions.RequestException as e:
                print(f"Error migrating cart: {e}")

        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        })


class LogoutView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            # Blacklist the refresh token in Redis
            cache.set(f"blacklisted_{refresh_token}", "true", timeout=settings.TOKEN_BLACKLIST_CACHE_TIMEOUT)
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

class TokenBlacklistCheck(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        token = request.data.get("token")
        is_blacklisted = cache.get(f"blacklisted_{token}")
        if is_blacklisted:
            return Response({"detail": "Token is blacklisted"}, status=status.HTTP_401_UNAUTHORIZED)
        return Response({"detail": "Token is valid"}, status=status.HTTP_200_OK)