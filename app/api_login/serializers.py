from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from own_modules.login import UserMessage
from rest_framework.response import Response
from django.contrib.auth.models import AbstractBaseUser
class CreateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'username', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self):
        self.is_valid()
        validated_data = self.validated_data
        user = User(
            email=validated_data['email'],
            username=validated_data['username']
        )
        user.set_password(validated_data['password'])
        user.save()
        token = Token.objects.create(user=user)
        return user
    def message(self):
        try:
            usr = self.create()
            msg = UserMessage().messageStatus[100]
            msg[0]["user"] = self.data["username"]
            return Response(msg[0], msg[1])
        except:
            msg = UserMessage().messageStatus[101]
            msg[0]["user"] = self.data["username"]
            msg[0]["error"] = self.errors
            return Response(msg[0], msg[1])


class LoginUserSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=100)
    password = serializers.CharField(max_length=100)

    def login(self):
        self.is_valid()
        validated_data =self.validated_data
        user = User.objects.filter(
            username=validated_data['username']
        )
        if len(user) == 1:
            user = user[0]
            password_auth = user.check_password(validated_data['password'])
            return [password_auth,user]
        return [False, None]


    def message(self):

            accept = self.login()
            response = UserMessage().login_success(accept[0],accept[1])
            return Response(response[0],response[1])

     #        msg = UserMessage().messageStatus[99]
       #      return Response(msg[0], msg[1])
