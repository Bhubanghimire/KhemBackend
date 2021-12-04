from django.urls import path, include
from .views import Refresh, Userlogin, SignUpOTPAPIView,RegisterAPIView

urlpatterns = [
    path("signup-otp/", SignUpOTPAPIView.as_view()),
    path("register/",RegisterAPIView.as_view()),
    path("login/", Userlogin.as_view()),
    path("refresh/",Refresh.as_view()),
]