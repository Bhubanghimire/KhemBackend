from django.urls import path, include
from .views import HighLightsAPIView,ReviewAPIVIew,GetReviewAPIView

urlpatterns = [
    path("highlights/", HighLightsAPIView.as_view()),
    path("add-review/",ReviewAPIVIew.as_view()),
    path("get-review/<int:project_id>/",GetReviewAPIView.as_view()),
]