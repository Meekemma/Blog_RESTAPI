from django.shortcuts import render, redirect  
from rest_framework.decorators import api_view  
from rest_framework.response import Response  
from rest_framework import status 
from .serializers import RegistrationSerializer, LoginSerializer  

# JWT authentication imports
from rest_framework_simplejwt.tokens import RefreshToken  
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer  
from rest_framework_simplejwt.views import TokenObtainPairView  

from django.contrib.auth import get_user_model  

User = get_user_model()  
from .models import *  


@api_view(['POST'])
def registration_view(request):
    """Handles user registration"""

    if request.method == 'POST':
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def login_view(request):
    """Handles user login and returns JWT tokens"""

    if request.method == 'POST':
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.validated_data['user']
            refresh = RefreshToken.for_user(user)  # Generate JWT tokens
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                "user_id": user.id,  
                "full_name": f"{user.first_name} {user.last_name}",
                "email": user.email,
                "is_verified": user.is_verified,
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
