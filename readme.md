
# 도로 날씨 변경 알림 서비스

  

## <들어가기전>

  

보내주신 [기상청_CCTV 기반 도로날씨정보 조회서비스](https://www.data.go.kr/data/15057966/openapi.do)에 문제가 2가지가 있었습니다.

  

### 문제1

  

OpenAPI를 제공하는 서버가 에러가 발생하였습니다. 2022/12/21시점에서 똑바른 요청을 한 결과

  

상태코드는 200이지만 Response(code: 03, result: Nodata)을 반환하는 문제(모든CCTV)가 있었습니다.

  

API제공측에 전화로 문의한 결과 현재 API내부에 문제를 확인하였다고 하였습니다.

  

2022/12/22시점에서 API내부의 문제를 해결하였다고 하였으나

  

일부 CCTV에 대한 요청으로는 아직도 에러가 있는 상황입니다.

  

### 문제2

  

기상청_CCTV 기반 도로날씨정보 조회서비스 요청사항에 대해서 문제가 있었습니다.

  

CCTV 요청사항은 아래와 같습니다.

  

***serviceKey, pageNo, numOfRows, dataType, hhCode***

  

요청사항중 ***pageNo, numOfRows hhCode***이 필수로 요구되지만 결과로써는 의미없는 Key값입니다.

  

담당자에게 연락하여 확인한 결과 과거의 데이터는 검색 할 수없고 현재 날씨만 요청이 가능하다고 연락을 받았습니다.

***이외***

개인적으로 알기 쉬운 디렉토리구조로 바꾸었습니다. Django의 디렉토리구조와는 조금 다를수있습니다.

  

## <기능>

  

* User등록(post: users/sign-up)   
params   
email: str   

  

* User정보(get: users/<int:id>)
  

* CCTV(seed)

  

* CCTV목록(get: CCTVs)
  

* CCTV구독 (post: users/<int:id>/cctv-subscribe)   
params    
cctvs_ids: list   
remove_cctv_ids: list   
  

* View테스트코드작성

  

* 날씨변경시 메일전송(스케줄링)

  
  

## <문제접근>

  

문제: 과거날씨와 현재날씨가 바뀌었을 경우 유저에게 메일을 발송 시스템(CCTV OpenAPI활용)

  

1. 유저에게 메일을 보내야함으로 User모델이 필요함.

  

2. CCTV OpenAPI를 확인해보니 많은 CCTV가 있다. 이 많은 CCTV가 날씨가 변경될때마다 User에게 메일을 발송하는 것은 좋지 않으므로 User이 CCTV를 구독하는 형식으로 문제접근

  

3. 한 User은 많은 CCTV를 구독 할 수 있어야하고 한 CCTV도 여러 User을 참조 할 수있어야 하므로 CCTV모델이 필요하고 User와 CCTV는 Many To Many의 관계를 맺어야한다.

  

4. CCTV 기반 도로날씨정보가이드에 CCTV_ID가 기입 되어있으므로 가이드의 CCTV_ID를 토대로 CCTV Seed데이터 작성(Master Data로 활용)

  

5. User은 CCTV를 구독하는 기능 작성

  

6. 날씨가 변경되는 것을 알기위해서는 주기적으로 과거의 날씨와 현재의 날씨를 비교를 하면 된다고생각하므로 스케줄링을 채택

  

7. 날씨를 DB에 저장하여 과거날씨와 현재날씨를 비교하는 것도 좋다고 생각하지만 간단하고 빠르게 Cache를 이용하여 DB조회없이 과거날씨와 현재날씨가 다르다면 CCTV를 구독한 User에게 메일발송


### 실행방법

1. 실행전 format.env를 참고하여 .env파일을 작성하여주세요.   
2. 실행전 ```python manage.py seed_cctv```를 실행하여 cctv seed데이터를 생성해주세요.   
3. 서버가동시 ```python manage.py runserver --noreload```로 실행시켜주세요(스케줄링 두번 기동하는 문제)   