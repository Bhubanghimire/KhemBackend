from .models import User
import jwt
from rest_framework.authentication import BaseAuthentication
from rest_framework import exceptions
from django.conf import settings


class SafeJWTAuthentication(BaseAuthentication):
    def authenticate (self, request):
        authorization_header = request.headers.get('Authorization')
        if not authorization_header:
            return None

        try:
            access_token = authorization_header.split(' ')[1]
            payload = jwt.decode(access_token, settings.SECRET_KEY, algorithms=['HS256'])

        except jwt.ExpiredSignatureError:
            raise exceptions.AuthenticationFailed('access_token expired')
        except IndexError:
            raise exceptions.AuthenticationFailed('Token prefix missing')
        except Exception:
            raise exceptions.AuthenticationFailed("Invalid Access Token")

        u_id=payload['user_id']
        user = User.objects.filter(id=u_id)

        if len(user)==0:
            raise exceptions.AuthenticationFailed('User not found')

        user=User.objects.get(id=u_id)
        if not user.is_active:
            raise exceptions.AuthenticationFailed('user is inactive')
        return user, None