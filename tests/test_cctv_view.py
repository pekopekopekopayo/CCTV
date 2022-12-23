import pdb
from rest_framework.test import APITestCase
from models.cctv.models import Cctv

from models.user.models import User


class CctvViewTest(APITestCase):
    def setUp(self):
        Cctv.objects.create(id="123123", road_name="test_road")
        Cctv.objects.create(id="456456", road_name="test_road2")

    def test_get(self):
        response = self.client.get("/cctvs")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), len(Cctv.objects.all()))
        self.assertIsInstance(response.data, list)
