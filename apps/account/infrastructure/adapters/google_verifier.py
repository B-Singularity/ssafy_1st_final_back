from django.conf import settings
from google.oauth2 import id_token
from google.auth.transport import requests

from apps.account.application.ports.social_verifier import SocialTokenVerifier, SocialUserInfo


class GoogleTokenVerifier(SocialTokenVerifier):
    def verify(self, token) -> SocialUserInfo:
        try:
            client_id = getattr(settings, "GOOGLE_CLIENT_ID", None)
            if not client_id:
                raise ValueError("GOOGLE_CLIENT_ID가 서버에 설정되어 있지 않습니다.")

            id_info = id_token.verify_oauth2_token(
                token, requests.Request(), client_id, clock_skew_in_seconds=5
            )

            verified_google_user_id = id_info.get('sub')
            verified_email = id_info.get('email')

            if not verified_google_user_id or not verified_email:
                raise ValueError("Google 토큰에서 필수 사용자 정보를 얻을 수 없습니다.")

            return SocialUserInfo(
                social_id=verified_google_user_id,
                email=verified_email,
                nickname=id_info.get('name', '')
            )
        except ValueError as e:
            raise ValueError(f"Google ID 토큰 검증 실패: {str(e)}")
