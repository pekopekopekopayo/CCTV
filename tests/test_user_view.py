import pdb
from rest_framework.test import APITestCase
from models.cctv.models import Cctv

from models.user.models import User


class UserViewTest(APITestCase):
    def setUp(self):
        Cctv.objects.create(id="123123", road_name="test_road")
        Cctv.objects.create(id="456456", road_name="test_road2")

    def test_sign_up(self):
        params = {"email": "test@test.com"}
        response = self.client.post("/users/sign-up", params)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data["email"], params["email"])
        self.assertTrue(User.objects.filter(email=params["email"]).exists())

    def test_sign_up_fail_case(self):
        params = {"email": "it is not email"}
        response = self.client.post("/users/sign-up", params)

        self.assertEqual(response.status_code, 400)
        self.assertFalse(User.objects.filter(email=params["email"]).exists())

    def test_show(self):
        user = User.objects.create(email="test@test.com")
        response = self.client.get(f"/users/{user.id}")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["email"], user.email)
        self.assertIsInstance(response.data["cctvs"], list)

    def test_show_fail_case(self):
        response = self.client.get(f"/users/{123}")

        self.assertEqual(response.status_code, 404)

    def test_cctv_subscribe(self):
        remove_cctv = Cctv.objects.create(id="789789", road_name="test_road3")
        user = User.objects.create(email="test@test.com")
        user.cctvs.add(remove_cctv)

        params = {
            "cctv_ids": Cctv.objects.exclude(id=remove_cctv.id).values_list("id", flat=True),
            "remove_cctv_ids": [remove_cctv.id],
        }
        response = self.client.post(f"/users/{user.id}/cctv-subscribe", params, format="json")

        self.assertEqual(response.status_code, 200)
        self.assertFalse(user.cctvs.filter(id=remove_cctv).exists())
        self.assertTrue(len(user.cctvs.filter(id__in=params["cctv_ids"])) == len(params["cctv_ids"]))
