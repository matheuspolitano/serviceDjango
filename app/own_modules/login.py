from rest_framework import status
from rest_framework.permissions import BasePermission,IsAuthenticated
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import update_last_login
from rest_framework.authentication import get_authorization_header
__all__ = ["UserMessage"]


class UserMessage:
    def __init__(self):
        self.messageStatus = {
            101:[
                {"message":"Not create user"},status.HTTP_400_BAD_REQUEST
            ],
            100:[
                {"message":"Create user"},status.HTTP_201_CREATED
            ],
            103:[
                {"message":"Not login"},status.HTTP_401_UNAUTHORIZED
            ],
            102:[
                {"message":"Login success"},status.HTTP_202_ACCEPTED
            ],
            99: [
                {"message": "Error server"}, status.HTTP_500_INTERNAL_SERVER_ERROR
            ]
        }
    def login_success(self,success,user=None):
        print(success)
        if success:
            token = Token.objects.filter(user=user)
            if len(token) == 1:
                update_last_login(sender=None,user=user)
                token = token[0]
                response = self.messageStatus[102]
                response[0]["token"] = token.key
                return response
            else:
                response = self.messageStatus[103]
                response[0]["error"] = "Token dont register"
                return response

        return self.messageStatus[103]



class LoginPermission(BasePermission):

    def has_permission(self, request, view):
        if request.method == "POST":
            return True

def get_token_user(request):
    token = get_authorization_header(request).split()[1].decode()
    token = Token.objects.filter(key=token)
    if len(token) > 0:
        return token[0].user

class RegisterPermission(IsAuthenticated):

    def has_permission(self, request, view):
        permission = super().has_permission(request,view)
        if request.method == "POST" and permission:
            user = get_token_user(request)
            if user.is_superuser:
                return True

        return False





