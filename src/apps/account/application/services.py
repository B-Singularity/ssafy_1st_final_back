import logging
from typing import Optional, Dict, Type
from django.db import transaction
from django.utils import timezone
from dependency_injector import providers

from .ports.auth_token import AuthTokenService
from .ports.social_verifier import SocialTokenVerifier
from .dtos import (
    UserAccountDto, UpdateNicknameRequestDto, UserSocialLinkDto,
    AuthResponseDto, SocialLoginRequestDto, LogoutRequestDto
)
from ..domain.repositories import UserAccountRepository
from ..domain.aggregates.user_account import UserAccount
from ..domain.value_objects.email import Email
from ..domain.value_objects.nickname import NickName
from ..domain.value_objects.social_link import SocialLink

logger = logging.getLogger(__name__)


class UserAuthAppService:
    def __init__(self,
                 user_account_repository: UserAccountRepository,
                 social_verifier_map: Dict[str, providers.Provider],
                 token_service: AuthTokenService):
        self.user_account_repository = user_account_repository
        self.social_verifier_map = social_verifier_map
        self.token_service = token_service

    def _map_domain_to_dto(self, user_account: UserAccount) -> UserAccountDto:
        social_links_dto = [
            UserSocialLinkDto(provider_name=link.provider_name, social_id=link.social_id)
            for link in user_account.social_links
        ]
        return UserAccountDto(
            account_id=user_account.account_id,
            email=user_account.email.address,
            nickname=user_account.nickname.name,
            social_links=social_links_dto,
            created_at=user_account.created_at,
            last_login_at=user_account.last_login_at,
        )

    @transaction.atomic
    def login_or_register(self, request_dto: SocialLoginRequestDto) -> AuthResponseDto:
        provider = request_dto.provider.lower()
        verifier_factory = self.social_verifier_map.get(provider)
        if not verifier_factory:
            raise ValueError(f"지원하지 않는 소셜 로그인 제공자입니다: {provider}")

        verifier: SocialTokenVerifier = verifier_factory()
        verified_info = verifier.verify(request_dto.id_token)

        social_link_vo = SocialLink(provider_name=provider, social_id=verified_info.social_id)
        email_vo = Email(verified_info.email)

        user_account = self.user_account_repository.find_by_social_link(social_link_vo)
        is_new_user = False
        current_time = timezone.now()

        if user_account:
            logger.info(f"기존 소셜 계정으로 로그인합니다. account_id: {user_account.account_id}")
            user_account.record_login(current_time)
        else:
            user_account = self.user_account_repository.find_by_email(email_vo)
            if user_account:
                logger.info(f"기존 이메일 계정에 소셜 링크를 추가합니다. account_id: {user_account.account_id}")
                user_account.add_social_link(social_link_vo)
                user_account.record_login(current_time)
            else:
                logger.info(f"신규 사용자를 생성합니다. email: {email_vo.address}")
                is_new_user = True
                nickname_str = request_dto.nickname_suggestion or verified_info.nickname or email_vo.address.split('@')[
                    0]
                suggested_nickname = NickName(nickname_str)
                if self.user_account_repository.find_by_nickname(suggested_nickname):
                    raise ValueError(f"닉네임 '{suggested_nickname.name}'은 이미 사용 중입니다.")

                user_account = UserAccount(
                    account_id=0,
                    email=email_vo,
                    nickname=suggested_nickname,
                    social_links=[social_link_vo],
                    created_at=current_time,
                    last_login_at=current_time
                )

        saved_user_account = self.user_account_repository.save(user_account)
        tokens = self.token_service.issue_for_user(saved_user_account.account_id)
        user_dto = self._map_domain_to_dto(saved_user_account)

        return AuthResponseDto(
            access_token=tokens['access'],
            refresh_token=tokens['refresh'],
            user=user_dto,
            is_new_user=is_new_user
        )

    def logout_user(self, request_dto: LogoutRequestDto) -> None:
        self.token_service.blacklist(request_dto.refresh_token)


class UserProfileAppService:
    def __init__(self, user_account_repository: UserAccountRepository):
        self.user_account_repository = user_account_repository

    def _map_domain_to_dto(self, user_account: UserAccount) -> UserAccountDto:
        social_links_dto = [
            UserSocialLinkDto(provider_name=link.provider_name, social_id=link.social_id)
            for link in user_account.social_links
        ]
        return UserAccountDto(
            account_id=user_account.account_id,
            email=user_account.email.address,
            nickname=user_account.nickname.name,
            social_links=social_links_dto,
            created_at=user_account.created_at,
            last_login_at=user_account.last_login_at
        )

    @transaction.atomic
    def get_user_profile(self, account_id: int) -> Optional[UserAccountDto]:
        user_account = self.user_account_repository.find_by_id(account_id)
        if not user_account:
            return None
        return self._map_domain_to_dto(user_account)

    @transaction.atomic
    def update_user_nickname(self, account_id: int, request_dto: UpdateNicknameRequestDto) -> UserAccountDto:
        user_account = self.user_account_repository.find_by_id(account_id)
        if not user_account:
            raise ValueError("사용자를 찾을 수 없습니다.")

        new_nickname = NickName(request_dto.nickname)

        def is_nickname_unique(nickname_to_check: NickName, current_account_id: int) -> bool:
            existing_user = self.user_account_repository.find_by_nickname(nickname_to_check)
            return not (existing_user and existing_user.account_id != current_account_id)

        user_account.update_nickname(new_nickname, is_nickname_unique)
        updated_user_account = self.user_account_repository.save(user_account)
        return self._map_domain_to_dto(updated_user_account)


class UserAccountDeactivationAppService:
    def __init__(self, user_account_repository: UserAccountRepository):
        self.user_account_repository = user_account_repository

    @transaction.atomic
    def deactivate_account(self, account_id: int) -> None:
        self.user_account_repository.delete(account_id)