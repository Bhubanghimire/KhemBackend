from django.shortcuts import render
from .serializers import ChoiceSerializers
from common.models import ConfigChoice
from rest_framework.views import APIView
from rest_framework.response import Response


# Create your views here.
class HomeTypeAPIView(APIView):
    def get(self, request):
        home_type = ConfigChoice.objects.filter(category__type="HomeType")
        type_serializers = ChoiceSerializers(home_type, many=True).data
        response={
            "data":type_serializers,
            "message":"Home Type list"
        }
        return Response(response)