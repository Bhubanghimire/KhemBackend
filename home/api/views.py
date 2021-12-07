import json
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from home.models import Project,Facility,Gallery, Review,Estimation, Facility
from rest_framework.permissions import AllowAny,IsAuthenticated
from common.models import ConfigChoice
from django.db.models import Sum, Min, Avg
from accounts.api.serializers import UserSerializers
from .serializers import ProjectSerializers,FacilitySerializers, GallerySerializers, ReviewSerializers, EstimationSerializers, FacilitySerializers
User = get_user_model()


# Create your views here.
class HighLightsAPIView(APIView):
    def get(self, request):
        final_list=[]
        project_objs = Project.objects.all()
        project_serializers = ProjectSerializers(project_objs, many=True).data

        for project in project_serializers:
            id = project["id"]
            name = project["name"]
            gallery=Gallery.objects.filter(project=id).first()
            if gallery is not None:
                gallery_serializers = GallerySerializers(gallery, context={"request":request}).data
                image=gallery_serializers["image"]
            else:
                image = ""

            facility = Facility.objects.filter(project=id).first()
            if facility is not None:
                facility_serializer = FacilitySerializers(facility).data
            else:
                facility_serializer ={}

            final_json={
                "id":id,
                "name":name,
                "photo":image,
                "facilities":facility_serializer
            }
            final_list.append(final_json)
            

        response={
            "data":final_list,
            "message":"list of heightlights."
        }
        return Response(response)


class ReviewAPIVIew(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        data={}
        user=request.user.id
        data["project"]=request.data["project"]
        data["rated_by"] = user
        data["value"] = request.data["value"]
        data["comment"] = request.data["comment"]
        image=request.FILES.getlist("image")
        review_ser=ReviewSerializers(data=data)
        review_ser.is_valid(raise_exception=True)
        gallery=[]
        if review_ser.is_valid():
            review_ser.save()
            id=review_ser.data["id"]
            for i in range(len(image)):
                json_data = {
                    "image": image[i],
                    "review": id
                }
                gallery.append(json_data)
            image_ser=GallerySerializers(data=gallery, many=True)
            image_ser.is_valid(raise_exception=True)
            image_ser.save()
        
        response = {
            "data": review_ser.data,
            "message": "Review added successfully."
        }
        return Response(response)


class GetReviewAPIView(APIView):
    def get(self, request, project_id):
        image_list=[]
        final_list=[]
        review = Review.objects.filter(project=project_id)
        review_serializer = ReviewSerializers(review, many=True).data
        for review in review_serializer:
            id=review["id"]
            comment = review["comment"]
            value=review["value"]
            gallery=Gallery.objects.filter(review=id)
            gallery_serializers = GallerySerializers(gallery,many=True, context={"request":request}).data
            for gallery in gallery_serializers:
                image=gallery["image"]
                image_list.append(image)

            rated_by = review["rated_by"]
            user=User.objects.get(id=rated_by)
            user_ser=UserSerializers(user, context={"request":request}).data
            final_json={
                "id":id,
                "comment":comment,
                "value":float(value),
                "image":image_list,
                "comment_by":user_ser["name"],
                "profile":user_ser["profile"]
            }
            final_list.append(final_json)

        response ={
            "data":final_list,
            "message":"list of review."
        }
        return Response(response)


class ProjectDetailAPIView(APIView):
    def get(self, request,project_id):
        final_response={}
        project_obj = Project.objects.filter(id=project_id).first()
        if project_obj is None:
            return Response({"message":"No project available"},status=400)
        project_ser = ProjectSerializers(project_obj).data
        final_response["id"]=project_ser["id"]
        final_response["name"]=project_ser["name"]
        final_response["description"]=project_ser["description"]
        company_id = project_ser["company"]
        company =User.objects.get(id=company_id)
        company_json={
            "id":company_id,
            "name":str(company)
        }

        final_response["company"]=company_json
        family_type = project_ser["family_type"]
        type=ConfigChoice.objects.get(id=family_type)
        final_response["family_type"]=str(type)

        estimation=Estimation.objects.filter(project=project_id)
        estimation_ser=EstimationSerializers(estimation,many=True,context={"request":request}).data
        final_response["estimation"]=estimation_ser

        facility =Facility.objects.filter(project=project_obj).first()
        facility_ser = FacilitySerializers(facility).data
        final_response["facility"]=facility_ser

        rating=Review.objects.filter().aggregate(Avg('value'))
        rate=rating["value__avg"]
        final_response["rate"]=rate

        response={
            "data":final_response,
            "message":"detail of project"
        }
        return Response(response)