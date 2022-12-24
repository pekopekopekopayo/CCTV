from django.db import transaction
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.decorators import api_view
from models.cctv.models import Cctv
from models.user.models import User
from serializer.user_serializer import CctvSubscriptSerializer, UserSerializer


class UserView:
    @api_view(["POST"])
    def sign_up(req):
        user_serializer = UserSerializer(data=req.data)

        if user_serializer.is_valid():
            user_serializer.save()
            return Response(user_serializer.data, status=201)
        else:
            return Response(user_serializer.errors, status=400)

    @api_view(["GET"])
    def show(req, id):
        user = get_object_or_404(User, id=id)

        serializer = CctvSubscriptSerializer(instance=user)
        return Response(serializer.data, status=200)

    @api_view(["POST"])
    def cctv_subscribe(req, id):
        user = get_object_or_404(User, id=id)

        add_cctvs = Cctv.objects.filter(id__in=req.data.get("cctv_ids"))
        remove_cctvs = Cctv.objects.filter(id__in=req.data.get("remove_cctv_ids"))

        with transaction.atomic():
            user.cctvs.remove(*remove_cctvs)
            user.cctvs.add(*add_cctvs)

        serializer = CctvSubscriptSerializer(instance=user)
        return Response(serializer.data, status=200)
