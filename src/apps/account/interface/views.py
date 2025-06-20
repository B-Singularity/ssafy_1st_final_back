from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from dependency_injector.wiring import inject, Provide

from .serializers import (
    SocialLoginRequestSerializer, AuthResponseSerializer, UserAccountResponseSerializer,
    UpdateNicknameRequestSerializer, LogoutRequestSerializer
)
from ..application.dtos import SocialLoginRequestDto, UpdateNicknameRequestDto, LogoutRequestDto
from ..application.services import (
    UserAuthAppService, UserProfileAppService, UserAccountDeactivationAppService
)
from ..containers import AccountContainer

import logging
logger = logging.getLogger(__name__)

class SocialLoginAPIView(APIView):
    @inject
    def post(self, request,
             service: UserAuthAppService = Provide[AccountContainer.user_auth_service]):
        serializer = SocialLoginRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        dto = SocialLoginRequestDto(**serializer.validated_data)
        try:
            auth_response_dto = service.login_or_register(dto)
            response_serializer = AuthResponseSerializer(auth_response_dto)

            user_info = auth_response_dto.user
            logger.info(
                f"소셜 로그인/회원가입 성공. user_id: {user_info.account_id}, is_new: {auth_response_dto.is_new_user}"
            )
            return Response(response_serializer.data, status=status.HTTP_200_OK)
        except ValueError as e:
            logger.warning(f"소셜 로그인 비즈니스 로직 오류: {e}", extra={'request_data': request.data})
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f"소셜 로그인 처리 중 예상치 못한 서버 오류 발생", exc_info=True)
            return Response({"error": f"서버 내부 오류: {e}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class LogoutAPIView(APIView):
    permission_classes = [IsAuthenticated]
    @inject
    def post(self, request,
             service: UserAuthAppService = Provide[AccountContainer.user_auth_service]):
        logger.info(f"로그아웃 요청 수신: user_id: {request.user.id}")
        serializer = LogoutRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        dto = LogoutRequestDto(**serializer.validated_data)

        try:
            service.logout_user(dto)
            logger.info(f"사용자 로그아웃 성공. user_id: {request.user.id}")
            return Response({"detail": "성공적으로 로그아웃되었습니다."}, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(f"로그아웃 처리 중 예상치 못한 오류 발생. user_id: {request.user.id}", exc_info=True)
            return Response({"error": "로그아웃 처리 중 오류가 발생했습니다."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class UserProfileAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @inject
    def get(self, request,
            service: UserProfileAppService = Provide[AccountContainer.user_profile_service]):

        account_id = request.user.id
        logger.info(f"프로필 조회 요청. user_id: {account_id}")

        profile_dto = service.get_user_profile(account_id)
        if profile_dto:
            serializer = UserAccountResponseSerializer(profile_dto)
            return Response(serializer.data)

        logger.warning(f"프로필을 찾을 수 없음. user_id: {account_id}")
        return Response({"error": "프로필을 찾을 수 없습니다."}, status=status.HTTP_404_NOT_FOUND)

    @inject
    def patch(self, request,
              service: UserProfileAppService = Provide[AccountContainer.user_profile_service]):

        account_id = request.user.id
        logger.info(f"닉네임 변경 요청. user_id: {account_id}")

        serializer = UpdateNicknameRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        dto = UpdateNicknameRequestDto(**serializer.validated_data)

        try:
            updated_profile = service.update_user_nickname(account_id, dto)
            response_serializer = UserAccountResponseSerializer(updated_profile)
            logger.info(f"닉네임 변경 성공. user_id: {account_id}")
            return Response(response_serializer.data)
        except ValueError as e:
            logger.warning(f"닉네임 변경 비즈니스 오류: {e}", extra={'request_data': request.data})
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f"닉네임 변경 중 예상치 못한 서버 오류 발생. user_id: {account_id}", exc_info=True)
            return Response({"error": "프로필 업데이트 중 오류가 발생했습니다."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class UserDeactivationAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @inject
    def delete(self, request,
               service: UserAccountDeactivationAppService = Provide[AccountContainer.user_deactivation_service]):

        account_id = request.user.id
        logger.info(f"회원 탈퇴 요청. user_id: {account_id}")

        try:
            service.deactivate_account(account_id)
            logger.info(f"회원 탈퇴 성공. user_id: {account_id}")
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            logger.error(f"회원 탈퇴 처리 중 예상치 못한 오류 발생. user_id: {account_id}", exc_info=True)
            return Response({"error": "회원 탈퇴 처리 중 오류가 발생했습니다."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
