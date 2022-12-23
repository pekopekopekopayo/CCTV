import pdb
from rest_framework import serializers
from models.user.models import User
from serializer.cctv_serializer import CctvSerializer


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["email"]

    def create(self, validated_data):
        return User.objects.create(**validated_data)


class CctvSubscriptSerializer(serializers.ModelSerializer):
    cctvs = CctvSerializer(many=True)

    class Meta:
        model = User
        fields = ["email", "cctvs"]
