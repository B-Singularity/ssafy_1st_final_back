from rest_framework import serializers
from apps.account.application.dtos import UserSocialLinkDto, UserAccountDto


class SocialLoginRequestSerializer(serializers.Serializer):
    provider = serializers.CharField() # 'google' 값이 들어올 것임
    id_token = serializers.CharField(required=True) # Google ID 토큰
    email = serializers.EmailField(required=True) # Vue에서 보낸 사용자 이메일 (Google에서 받은 값)
    nickname_suggestion = serializers.CharField(required=False, allow_blank=True, max_length=15, allow_null=True)

class UpdateNicknameRequestSerializer(serializers.Serializer):
    nickname = serializers.CharField(required=True, min_length=2, max_length=15)

class UserSocialLinkResponseSerializer(serializers.Serializer):
    provider_name = serializers.CharField()
    social_id = serializers.CharField()

class UserAccountResponseSerializer(serializers.Serializer):
    # 이 시리얼라이저는 Users 모델 인스턴스 또는 UserAccountDto 도메인 객체를 받아 직렬화합니다.
    # 서비스 계층에서 UserAccountDto를 생성하여 이 시리얼라이저로 넘겨주면 됩니다.
    account_id = serializers.IntegerField(read_only=True) # Users 모델의 id
    email = serializers.EmailField(read_only=True) # Users 모델의 email_address
    nickname = serializers.CharField(read_only=True) # Users 모델의 nickname
    social_links = UserSocialLinkResponseSerializer(many=True, read_only=True) # 연결된 소셜 계정 정보
    created_at = serializers.DateTimeField(read_only=True)
    last_login_at = serializers.DateTimeField(read_only=True, allow_null=True)

class AuthResponseSerializer(serializers.Serializer):
    # [확인] 이 형식으로 최종 응답이 나갈 것임
    access_token = serializers.CharField()
    refresh_token = serializers.CharField()
    user = UserAccountResponseSerializer() # UserAccountResponseSerializer를 중첩하여 사용자 정보 포함
    is_new_user = serializers.BooleanField()

class LogoutRequestSerializer(serializers.Serializer):
    refresh_token = serializers.CharField(required=True)