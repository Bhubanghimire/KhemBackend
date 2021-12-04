from rest_framework.response import Response
import jwt
from rest_framework import serializers
from django.contrib.auth import login, authenticate
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_401_UNAUTHORIZED,
    HTTP_400_BAD_REQUEST
)
from rest_framework.permissions import AllowAny,IsAuthenticated
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from rest_framework.views import APIView
from rest_framework import exceptions
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.contrib.auth import get_user_model
from accounts.Middleware import generate_access_token, generate_refresh_token, generateOTP
from accounts.models import OTP
from .serialializers import UserSerializers

User=get_user_model()


# Create your views here.
class Refresh(APIView):
    permission_classes = [IsAuthenticated,]

    def get(self, request):
        token = request.headers.get('refreshtoken')
        if token is None:
            return Response({"message":"please send refreshtoken in header"}, status=HTTP_400_BAD_REQUEST)

        try:
            payload= jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise exceptions.AuthenticationFailed('Refresh Token expired')

        except Exception:
            raise exceptions.AuthenticationFailed("Invalid Refresh Token")

        user = User.objects.filter(id=payload.get('user_id')).first()
        if user is None:
            raise exceptions.AuthenticationFailed('User not found')

        if not user.is_active:
            raise exceptions.AuthenticationFailed('user is inactive')

        access_token = generate_access_token(user)
        refresh_token=generate_refresh_token(user)
        response = {
            "data":
                {
                    "access_token": access_token,
                    "refresh_refresh": refresh_token,
                },
            "message": "New Generated Credentials."
        }
        return Response(response)


class Userlogin(APIView):

    def post(self, request):
        password = request.data.get('password', 'None')
        email = request.data.get('email', "None")

        if email=="None" or password=="None":
            raise serializers.ValidationError(
                {"message": "Enter Email and password"}
            )

        else:
            user = authenticate(request, email=email, password=password)
            if user is None:
                raise serializers.ValidationError(
                    {"message":"A user with this email and password was not found."}
                )

            access_token = generate_access_token(user)
            refresh_token = generate_refresh_token(user)

            response = {
                "data":
                    {
                        "access_token": access_token,
                        "refresh_refresh": refresh_token,
                    },
                "message": "loggedIn successfully."
            }
            return Response(response, status=HTTP_200_OK)


class SignUpOTPAPIView(APIView):

    def post(self, request):
        data = request.data
        email = data['email']
        generate_otp = generateOTP()
        check_status = OTP.objects.filter(email=email)

        if len(check_status)>0:
            check_status.update(otp=generate_otp)
            html_content = render_to_string("email_template.html", {'title': 'Otp', 'contend': generate_otp})
            test_contend = strip_tags(html_content)
            email = EmailMultiAlternatives('Otp for email verification', test_contend, settings.DEFAULT_FROM_EMAIL,
                                           [email])
            email.attach_alternative(html_content, 'text/html')
            try:
                email.send()
            except Exception:
                return Response({"message":"Email not sending.Try again."}, status=HTTP_400_BAD_REQUEST)
        else:
            OTP.objects.create(email=email, otp=generate_otp)
            html_content = render_to_string("email_template.html", {'title': 'Otp', 'contend': generate_otp})
            test_contend = strip_tags(html_content)
            email = EmailMultiAlternatives('Otp for email verification', test_contend, settings.DEFAULT_FROM_EMAIL,
                                           [email])
            email.attach_alternative(html_content, 'text/html')
            try:
                email.send()
            except Exception:
                return Response({"message":"Email not sending.Try again."}, status=HTTP_400_BAD_REQUEST)

        return Response({'message': 'OTP is sent to provided mail.'})


class RegisterAPIView(APIView):
    def post(self, request):
        data = request.data
        check_otp = OTP.objects.get(email=data['email'])
        check_user_already_exist = User.objects.filter(email=data['email'])
        if check_user_already_exist:
            return Response({'message': 'User already exist'}, status=HTTP_400_BAD_REQUEST)

        if check_otp.otp == data['otp']:
            user_serializers = UserSerializers(data=data)
            user_serializers.is_valid(raise_exception=True)
            if user_serializers.is_valid():
                user_serializers.save()
                check_otp.delete()
                id=user_serializers.data["id"]
                user=User.objects.get(id=id)
                access_token=generate_access_token(user)
                refresh_token=generate_refresh_token(user)
                response = {
                    "data":
                        {
                            "access_token": access_token,
                            "refresh_refresh": refresh_token,
                        },
                    "message": "loggedIn successfully."
                }
            return Response(response)
        else:
            return Response({'message': 'Otp is not matched'}, status=HTTP_400_BAD_REQUEST)




