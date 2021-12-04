from django.urls import path, include
from .views import HomeTypeAPIView

urlpatterns = [
    path("home-type/",HomeTypeAPIView.as_view()),
    ]