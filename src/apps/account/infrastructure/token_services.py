from typing import Dict
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError
from src.apps.account.models import Users

from src.apps.account.application.ports.auth_token import AuthTokenService


class SimpleJwtTokenService(AuthTokenService):
    def issue_for_user(self, user_account_id) -> Dict[str, str]:
        try:
            user_model = Users.objects.get(id=user_account_id)
            refresh = RefreshToken.for_user(user_model)
            return {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }
        except Users.DoesNotExist:
            raise ValueError("토큰을 발급할 사용자를 찾을 수 없습니다.")

    def blacklist(self, refresh_token: str) -> None:
        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
        except TokenError:
            pass