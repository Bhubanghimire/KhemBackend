from rest_framework import serializers
from home.models import Project, Gallery,Facility, Review,Estimation,Facility


class ProjectSerializers(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields ="__all__"


class FacilitySerializers(serializers.ModelSerializer):
    class Meta:
        model = Facility
        fields ="__all__"


class GallerySerializers(serializers.ModelSerializer):
    class Meta:
        model = Gallery
        fields ="__all__"


class ReviewSerializers(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields ="__all__"


class EstimationSerializers(serializers.ModelSerializer):
    class Meta:
        model =Estimation
        fields="__all__"


class FacilitySerializers(serializers.ModelSerializer):
    class Meta:
        model = Facility
        fields ="__all__"