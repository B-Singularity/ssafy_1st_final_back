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

class SocialLoginAPIView(APIView):
    @inject
    def post(self, request,
             service: UserAuthAppService = Provide[AccountContainer.user_auth_service]):
        serializer = SocialLoginRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        dto = SocialLoginRequestDto(**serializer.validated_data)
        try:
            auth_reponse_dto = service.login_or_register(dto)
            response_serializer = AuthResponseSerializer(auth_reponse_dto)
            return Response(response_serializer.data, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": f"서버 내부 오류: {e}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class LogoutAPIView(APIView):
    permission_classes = [IsAuthenticated]
    @inject
    def post(self, request,
             service: UserAuthAppService = Provide[AccountContainer.user_auth_service]):
        serializer = LogoutRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        dto = LogoutRequestDto(**serializer.validated_data)
        service.logout_user(dto)
        return Response({"detail": "성공적으로 로그아웃되었습니다."}, status=status.HTTP_200_OK)

class UserProfileAPIView(APIView):
    permission_classes = [IsAuthenticated]
    @inject
    def get(self, request,
            service: UserProfileAppService = Provide[AccountContainer.user_profile_service]):
        profile_dto = service.get_user_profile(request.user.id)
        if profile_dto:
            serializer = UserAccountResponseSerializer(profile_dto)
            return Response(serializer.data)
        return Response({"error": "프로필을 찾을 수 없습니다."}, status=status.HTTP_404_NOT_FOUND)

    @inject
    def patch(self, request,
             service: UserProfileAppService = Provide[AccountContainer.user_profile_service]):
        serializer = UpdateNicknameRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        dto = UpdateNicknameRequestDto(**serializer.validated_data)
        try:
            updated_profile = service.update_user_nickname(request.user.id, dto)
            response_serializer = UserAccountResponseSerializer(updated_profile)
            return Response(response_serializer.data)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

class UserDeactivationAPIView(APIView):
    permission_classes = [IsAuthenticated]
    @inject
    def delete(self, request,
               service: UserAccountDeactivationAppService = Provide[AccountContainer.user_deactivation_service]):
        service.deactivate_account(request.user.id)
        return Response(status=status.HTTP_204_NO_CONTENT)