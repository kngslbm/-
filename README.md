## *Internship Preonboarding Challenge Backend(Python)*

**DRF(Django REST framework)** 환경에서 **JWT** 기반의 회원 관리 로직입니다.

**Pytest** 프레임워크를 사용하여 **Test Case**를 작성하였습니다.

</br>

### API 명세
|Authorization|Request|Domain|Description|
|---|---|---|---|
|None|-|**`/admin/`**|관리자 페이지|
|None|POST|**`/api/v1/accounts/register/`**|회원 가입|
|Only Self|DELETE|**`/api/v1/accounts/register/`**|회원 탈퇴|
|None|POST|**`/api/v1/accounts/signin/`**|로그인|
|Only Self|POST|**`/api/v1/accounts/signout/`**|로그아웃|
|Only Self|POST|**`/api/v1/accounts/token/refresh/`**|토큰 리플래쉬|
|Only Self|PUT|**`/api/v1/accounts/change-password/`**|비밀번호 변경|
|User with Login|GET|**`/api/v1/accounts/<str:username>/`**|회원 정보 조회|
|User with Login|PUT|**`/api/v1/accounts/<str:username>/`**|회원 정보 변경|
