from rest_framework import serializers
from common.models import ConfigChoice


class ChoiceSerializers(serializers.ModelSerializer):
    class Meta:
        model = ConfigChoice
        fields = ["id","value","description"]