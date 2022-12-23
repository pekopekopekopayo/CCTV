from rest_framework import serializers
from models.cctv.models import Cctv


class CctvSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cctv
        fields = ["id", "road_name"]
