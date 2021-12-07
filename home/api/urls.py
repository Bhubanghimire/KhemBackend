from django.urls import path, include
from .views import HighLightsAPIView,ReviewAPIVIew,GetReviewAPIView,ProjectDetailAPIView

urlpatterns = [
    path("<int:project_id>/project/",ProjectDetailAPIView.as_view()),
    path("highlights/", HighLightsAPIView.as_view()),
    path("add-review/",ReviewAPIVIew.as_view()),
    path("get-review/<int:project_id>/",GetReviewAPIView.as_view()),
]