# import random
from django.core.mail import EmailMessage
from django.core.cache import cache
import requests
from app.settings import SERVIICE_KEY
from models.cctv.models import Cctv


def change_weather():
    url = "http://apis.data.go.kr/1360000/RoadWthrInfoService/getCctvStnRoadWthr"

    # OpenAPI의 사양에 대해서는 README에 문제1,2를 참고해주세요.
    params = {
        "serviceKey": SERVIICE_KEY,
        "pageNo": "1",
        "numOfRows": "10",
        "dataType": "JSON",
        "hhCode": "00",
    }

    for cctv in Cctv.objects.all():
        params["eqmtId"] = cctv.id
        response = requests.get(url, params=params)

        try:
            # 현재 날씨만 조회가능함.
            new_weather = response.json()["response"]["body"]["items"]["item"][0]["weatherNm"]

            # 테스트를 하고 싶다면 밑 코드를 주석을 지워주세요.
            # new_weather = random.random()
            print(f"{cctv.road_name}의 날씨:{new_weather}")
        except KeyError:
            print(f"{cctv.road_name}의 API요청에러 에러코드:{response.status_code}")
            continue

        # 만약 데이터가 없을경우에는 skip하고 cache에 정보를 저장
        if old_weather := cache.get(cctv.id):
            if old_weather != new_weather:
                EmailMessage(
                    f"{cctv.road_name}의 날씨정보가 갱신되었습니다.",
                    f"날씨가 {old_weather}에서 {new_weather}로 갱신되었습니다.",
                    to=cctv.users.values_list("email", flat=True),
                ).send()
        # 날씨는 항상 갱신
        cache.set(cctv.id, new_weather, None)
