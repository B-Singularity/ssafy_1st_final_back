from django.conf import settings
from google.oauth2 import id_token
from google.auth.transport import requests
from src.apps.account.application.ports.social_verifier import SocialTokenVerifier, SocialUserInfo

import logging

logger = logging.getLogger(__name__)


class GoogleTokenVerifier(SocialTokenVerifier):
    def verify(self, token) -> SocialUserInfo:
        logger.info("Google 토큰 검증 API 호출을 시작합니다.")
        try:
            client_id = getattr(settings, "GOOGLE_CLIENT_ID", None)
            if not client_id:
                logger.critical("CRITICAL: GOOGLE_CLIENT_ID가 서버에 설정되어 있지 않습니다.")
                raise ValueError("GOOGLE_CLIENT_ID가 서버에 설정되어 있지 않습니다.")

            id_info = id_token.verify_oauth2_token(
                token, requests.Request(), client_id, clock_skew_in_seconds=5
            )

            verified_google_user_id = id_info.get('sub')
            verified_email = id_info.get('email')

            if not verified_google_user_id or not verified_email:
                logger.warning(f"Google 토큰에 필수 정보가 누락되었습니다. email: {verified_email}")
                raise ValueError("Google 토큰에서 필수 사용자 정보를 얻을 수 없습니다.")

            logger.info(f"Google 토큰 검증 성공. social_id: {verified_google_user_id}")

            return SocialUserInfo(
                social_id=verified_google_user_id,
                email=verified_email,
                nickname=id_info.get('name', '')
            )
        except ValueError as e:
            logger.error(f"유효하지 않은 Google ID 토큰입니다: {e}", exc_info=True)
            raise ValueError(f"Google ID 토큰 검증 실패: {str(e)}")

        except Exception as e:
            logger.critical(f"Google 토큰 검증 중 예상치 못한 외부 통신 오류 발생", exc_info=True)
            raise Exception("Google 인증 서버와 통신 중 오류가 발생했습니다.")
