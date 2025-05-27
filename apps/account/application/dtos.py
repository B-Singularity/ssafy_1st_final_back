from datetime import datetime

class SocialLoginRequestDto:
    def __init__(self,
                provider,
                id_token,
                email,
                nickname_suggestion):
        if provider.lower() != "google":
            raise ValueError("현재 구글 소셜 로그인만 지원합니다.")
        if not id_token:
            raise ValueError("소셜 ID 토큰은 필수입니다.")
        if not email:
            raise ValueError("이메일 정보는 필수입니다.")
        
        self.provider = "google"
        self.id_token = id_token
        self.email = email
        self.nickname_suggestion = nickname_suggestion

class UpdateNicknameRequestDto:
    def __init__(self, nickname):
        if not nickname or not (2 <= len(nickname) <= 15):
            raise ValueError("닉네임은 2자 이상 15자 이하이어야 합니다.")
        self.nickname = nickname

class UserSocialLinkDto:
    def __init__(self, provider_name, social_id):
        self.provider_name = provider_name
        self.social_id = social_id


class UserAccountDto:
    def __init__(self, 
                 account_id, 
                 email, 
                 nickname, 
                 social_links,
                 created_at, 
                 last_login_at):
        self.account_id = account_id
        self.email = email
        self.nickname = nickname
        self.social_links = social_links
        self.created_at = created_at
        self.last_login_at = last_login_at

class AuthResponseDto:
    def __init__(self, access_token, refresh_token, user, is_new_user=False):
        self.access_token = access_token
        self.refresh_token = refresh_token
        self.user = user
        self.is_new_user = is_new_user


class LogoutRequestDto:
    def __init__(self, refresh_token):
        if not refresh_token:
            raise ValueError("Refresh token은 필수입니다.")
        self.refresh_token = refresh_token
