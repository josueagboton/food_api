from rest_framework import status
from rest_framework.pagination import PageNumberPagination

from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework_simplejwt.tokens import RefreshToken


from food.models import Food
from food.serializers import FoodSerializer

# Create your views here.

@api_view(['POST'])
def register(request):
    if request.method == 'POST':
        username = request.data.get('username')
        password = request.data.get('password')
        if not username or not password:
            return Response({'error': 'Please provide both username and password'}, status=status.HTTP_400_BAD_REQUEST)
        
        if User.objects.filter(username=username).exists():
            return Response({'error': 'Username already exists'}, status=status.HTTP_400_BAD_REQUEST)
        
        user = User.objects.create_user(username=username, password=password)
        return Response({'message': 'User created successfully'}, status=status.HTTP_201_CREATED)


@api_view(['POST'])
def login(request):
    username = request.data.get('username')
    password = request.data.get('password')
    user = authenticate(username=username, password=password)
    if user:
        refresh = RefreshToken.for_user(user)
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }, status=status.HTTP_200_OK)
    else:
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
    
@api_view(['GET'])
def my_profil(request):
    if request.method == 'GET':
        user = request.user
        print(user)
        # Maintenant, vous pouvez utiliser les attributs de l'utilisateur, par exemple :
        username = user.username
        email = user.email
        # Autres attributs selon votre modèle User personnalisé
        # ...
        return Response({'username': username})


@api_view(['POST'])
def logout(request):
     # Supprime le token pour déconnecter l'utilisateur
    if request.method == 'POST':
        request.user.auth_token.delete()
        return Response({'success': 'Successfully logged out'}, status=status.HTTP_200_OK),
