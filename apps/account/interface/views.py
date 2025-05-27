from django.core.serializers import serialize
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from .serializers import (
    SocialLoginRequestSerializer,
    AuthResponseSerializer,
    UserAccountResponseSerializer,
    UpdateNicknameRequestSerializer, LogoutRequestSerializer
)
from apps.account.application.dtos import SocialLoginRequestDto, UpdateNicknameRequestDto, LogoutRequestDto
from apps.account.application.services import (
    UserAuthAppService,
    UserProfileAppService,
    UserAccountDeactivationAppService
)
from apps.account.infrastructure.repositories import DjangoUserAccountRepository
from apps.account.infrastructure.token_services import TokenService

import traceback


def get_user_auth_service():
    repo = DjangoUserAccountRepository()
    token_service = TokenService()
    return UserAuthAppService(user_account_repository=repo, token_service=token_service)

class SocialLoginAPIView(APIView):
    def post(self, request):
        print(">>> SocialLoginAPIView.post() 메서드 시작 <<<")
        print("--- SocialLoginAPIView POST 요청 수신 ---")
        print("Request Data:", request.data) # 실제 수신 데이터 출력
        serializer = SocialLoginRequestSerializer(data=request.data)
        if serializer.is_valid():
            print("Serializer 유효성 검사 통과")
            request_dto = SocialLoginRequestDto(
                provider=serializer.validated_data['provider'],
                id_token=serializer.validated_data['id_token'],
                email=serializer.validated_data['email'],
                nickname_suggestion=serializer.validated_data.get('nickname_suggestion')
            )

            repository = DjangoUserAccountRepository()
            token_service = TokenService()
            service = UserAuthAppService(user_account_repository=repository, token_service=token_service)

            try:
                print(">>> UserAuthAppService.login_or_register_with_google 호출 직전 <<<")  # 디버그_1
                auth_response_dto = service.login_or_register_with_google(request_dto)
                print(">>> UserAuthAppService.login_or_register_with_google 호출 성공 <<<")  # 디버그_2
                response_serializer = AuthResponseSerializer(auth_response_dto)
                return Response(response_serializer.data, status=status.HTTP_200_OK)
            except ValueError as e:  # 값 객체 생성 오류, 닉네임 중복 등 애플리케이션 서비스에서 발생시킨 ValueError
                print(f"!!! ValueError 발생: {str(e)} !!!")  # 디버그_3
                import traceback
                traceback.print_exc()
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
            except Exception as e:  # 그 외 모든 예상치 못한 오류
                print(f"!!! 일반 Exception 발생: {type(e).__name__} - {str(e)} !!!")  # ⭐️ 디버그_4: 어떤 종류의 예외인지 출력
                import traceback
                traceback.print_exc()  # ⭐️ 터미널에 전체 트레이스백 출력
                return Response({"error": "인증 처리 중 내부 서버 오류가 발생했습니다. 서버 로그를 확인해주세요."},
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            print(">>> Serializer 유효성 검사 실패 <<<")  # 기존 디버깅 코드
            print("Serializer Errors:", serializer.errors)  # 기존 디버깅 코드
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LogoutAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = LogoutRequestSerializer(data=request.data)
        if serializer.is_valid():
            request_dto = LogoutRequestDto(
                refresh_token=serializer.validated_data['refresh_token']
            )
            service = get_user_auth_service()
            try:
                service.logout_user(request_dto)
                return Response({"detail": "성공적으로 로그아웃되었습니다."}, status=status.HTTP_200_OK)
            except ValueError as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
            except Exception as e:
                return Response({"error": "로그아웃 처리 중 오류가 발생했습니다."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class UserProfileAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get_user_profile_service(self):
        repo = DjangoUserAccountRepository()
        return UserProfileAppService(user_account_repository=repo)

    def get(self, request):
        service = self.get_user_profile_service()
        account_id = request.user.id

        profile_dto = service.get_user_profile(account_id)
        if profile_dto:
            serializer = UserAccountResponseSerializer(profile_dto)
            return Response(serializer.data)
        return Response({"error": "프로필을 찾을 수 없습니다."}, status=status.HTTP_404_NOT_FOUND)

    def patch(self, request):
        service = self.get_user_profile_service()
        account_id = request.user.id

        serializer = UpdateNicknameRequestSerializer(data=request.data)
        if serializer.is_valid():
            request_dto = UpdateNicknameRequestDto(nickname=serializer.validated_data['nickname'])
            try:
                updated_profile_dto = service.update_user_nickname(account_id, request_dto)
                response_serializer = UserAccountResponseSerializer(updated_profile_dto)
                return Response(response_serializer.data)
            except ValueError as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
            except Exception as e:
                return Response({"error": "프로필 업데이트 중 오류가 발생했습니다."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserDeactivationAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get_user_deactivation_service(self):
        repo = DjangoUserAccountRepository()
        return UserAccountDeactivationAppService(user_account_repository=repo)

    def delete(self, request):
        service = self.get_user_deactivation_service()
        account_id = request.user.id
        try:
            service.deactivate_account(account_id)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response({"error": "회원 탈퇴 처리 중 오류가 발생했습니다."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)