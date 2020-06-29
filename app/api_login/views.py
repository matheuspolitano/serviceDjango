from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from own_modules.login import LoginPermission, RegisterPermission, get_token_user
from .serializers import LoginUserSerializer, CreateUserSerializer


class LoginAPI(APIView):
    permission_classes = [LoginPermission,]
    def post(self,request):
        return LoginUserSerializer(data=request.data).message()

class RegisterAPI(APIView):
    permission_classes = [RegisterPermission,]
    def post(self,request):
        user = get_token_user(request)
        msg = CreateUserSerializer(data=request.data).message()
        return msg



# Create your views here.
