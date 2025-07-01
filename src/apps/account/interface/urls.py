# apps/account/interface/urls.py
from django.urls import path
# [확인] views.py의 위치에 따라 임포트 경로 확인 (보통 같은 디렉토리면 .views)
from .views import (
    SocialLoginAPIView,
    UserProfileAPIView,
    UserDeactivationAPIView,
    LogoutAPIView
)

# app_name = 'account_interface' # 네임스페이스 사용 시 (선택 사항)

urlpatterns = [
    # [확인] Vue에서 호출할 소셜 로그인 API 경로
    # 이 경로는 프로젝트 전체 URL 설정과 조합되어 /api/accounts/auth/login (예시)이 됩니다.
    path('auth/login', SocialLoginAPIView.as_view(), name='social_login_register'),
    
    path('auth/logout', LogoutAPIView.as_view(), name='user_logout'),
    path('users/me/profile', UserProfileAPIView.as_view(), name='user_profile'),
    path('users/me', UserDeactivationAPIView.as_view(), name='user_deactivate'),
]