from rest_framework.response import Response
from models.cctv.models import Cctv
from serializer.cctv_serializer import CctvSerializer
from rest_framework.views import APIView


class CctvView(APIView):
    def get(self, req):
        cctvs = Cctv.objects.all()
        serializer = CctvSerializer(instance=cctvs, many=True)
        return Response(serializer.data, status=200)
