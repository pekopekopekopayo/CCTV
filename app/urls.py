from django.urls import path
from views.cctv_view import CctvView

from views.user_view import UserView

urlpatterns = [
    # 회원가입
    path("users/sign-up", UserView.sign_up),
    # 유저정보
    path("users/<int:id>", UserView.show),
    # 유저cctv구독하기
    path("users/<int:id>/cctv-subscribe", UserView.cctv_subscribe),
    # cctv목록
    path("cctvs", CctvView.as_view()),
]
