from sqlite3 import DatabaseError

from src.apps.account.domain.aggregates.user_account import UserAccount
from src.apps.account.domain.value_objects.email import Email
from src.apps.account.domain.value_objects.nickname import NickName
from src.apps.account.domain.value_objects.social_link import SocialLink
from src.apps.account.domain.repositories import UserAccountRepository
from src.apps.account.models import Users, UserSocialAccounts

from typing import Optional
from django.db import transaction, IntegrityError

import logging

logger = logging.getLogger(__name__)

class DjangoUserAccountRepository(UserAccountRepository):

    def generate_next_id(self) -> int:
        raise NotImplementedError("ID is auto-generated by the database.")

    def _to_domain_object(self, user_model: Users) -> UserAccount:
        social_links_vo_list = []
        if user_model and hasattr(user_model, 'social_accounts'):  # Check if user_model is not None
            for link_model in user_model.social_accounts.all():
                social_links_vo_list.append(
                    SocialLink(provider_name=link_model.provider, social_id=link_model.provider_account_id)
                )

        return UserAccount(
            account_id=user_model.id,
            email=Email(user_model.email_address),
            nickname=NickName(user_model.nickname),
            social_links=social_links_vo_list,
            created_at=user_model.created_at,
            last_login_at=user_model.last_login_at
        )

    @transaction.atomic
    def save(self, user_account: UserAccount) -> UserAccount:
        user_model = None
        try:
            if user_account.account_id and user_account.account_id > 0:
                try:
                    user_model = Users.objects.get(id=user_account.account_id)
                    user_model.email_address = user_account.email.address
                    user_model.nickname = user_account.nickname.name
                    user_model.last_login_at = user_account.last_login_at
                    user_model.save(update_fields=['email_address', 'nickname', 'last_login_at'])
                    logger.info(f"사용자 정보를 업데이트했습니다. account_id: {user_model.id}")
                except Users.DoesNotExist:
                    logger.error(f"ID({user_account.account_id}) 사용자를 찾을 수 없어 업데이트에 실패했습니다.", exc_info=True)
                    raise ValueError(f"ID {user_account.account_id}를 가진 사용자가 존재하지 않아 업데이트할 수 없습니다.")
            else:
                user_model = Users.objects.create(
                    email_address=user_account.email.address,
                    nickname=user_account.nickname.name,
                    created_at=user_account.created_at,
                    last_login_at=user_account.last_login_at
                )
                logger.info(f"새로운 사용자를 생성했습니다. account_id: {user_model.id}")

            user_model.social_accounts.all().delete()
            for sl_vo_item in user_account.social_links:
                UserSocialAccounts.objects.create(
                    user=user_model,
                    provider=sl_vo_item.provider_name,
                    provider_account_id=sl_vo_item.social_id
                )
            logger.info(f"사용자의 소셜 링크 정보를 동기화했습니다. account_id: {user_model.id}")

            return self._to_domain_object(user_model)
        except IntegrityError as e:
            logger.error(f"사용자 저장 중 무결성 제약 조건 위반 발생: {e}", exc_info=True)
            raise ValueError("이미 존재하는 이메일 또는 닉네임입니다.")
        except DatabaseError as e:
            logger.critical(f"사용자 저장 중 심각한 데이터베이스 오류 발생", exc_info=True)
            raise Exception("데이터베이스 처리 중 오류가 발생했습니다.")



    @transaction.atomic
    def delete(self, account_id: int) -> None:
        try:
            user_model = Users.objects.get(id=account_id)
            user_model.delete()
            logger.info(f"사용자 정보를 삭제했습니다. account_id: {account_id}")
        except Users.DoesNotExist:
            logger.warning(f"삭제할 사용자(ID: {account_id})를 찾을 수 없어 작업을 건너뜁니다.")
            pass
        except DatabaseError as e:
            logger.error(f"사용자 삭제 중 데이터베이스 오류 발생: {e}", exc_info=True)
            raise Exception("데이터베이스 처리 중 오류가 발생했습니다.")

    def find_by_id(self, account_id: int) -> Optional[UserAccount]:
        try:
            user_model = Users.objects.prefetch_related('social_accounts').get(id=account_id)
            return self._to_domain_object(user_model)
        except Users.DoesNotExist:
            logger.debug(f"ID({account_id})에 해당하는 사용자를 찾을 수 없습니다.")
            return None
        except DatabaseError as e:
            logger.error(f"ID로 사용자 조회 중 데이터베이스 오류 발생: {e}", exc_info=True)
            raise Exception("데이터베이스 조회 중 오류가 발생했습니다.")

    def find_by_email(self, email: Email) -> Optional[UserAccount]:
        try:
            user_model = Users.objects.prefetch_related('social_accounts').get(email_address=email.address)
            return self._to_domain_object(user_model)
        except Users.DoesNotExist:
            logger.debug(f"Email({email.address})에 해당하는 사용자를 찾을 수 없습니다.")
            return None
        except DatabaseError as e:
            logger.error(f"Email로 사용자 조회 중 데이터베이스 오류 발생: {e}", exc_info=True)
            raise Exception("데이터베이스 조회 중 오류가 발생했습니다.")

    def find_by_nickname(self, nickname: NickName) -> Optional[UserAccount]:
        try:
            user_model = Users.objects.prefetch_related('social_accounts').get(nickname=nickname.name)
            return self._to_domain_object(user_model)
        except Users.DoesNotExist:
            logger.debug(f"Nickname({nickname.name})에 해당하는 사용자를 찾을 수 없습니다.")
            return None
        except DatabaseError as e:
            logger.error(f"Nickname으로 사용자 조회 중 데이터베이스 오류 발생: {e}", exc_info=True)
            raise Exception("데이터베이스 조회 중 오류가 발생했습니다.")

    def find_by_social_link(self, social_link: SocialLink) -> Optional[UserAccount]:
        try:
            link_model = UserSocialAccounts.objects.select_related('user').get(
                provider=social_link.provider_name,
                provider_account_id=social_link.social_id
            )
            return self._to_domain_object(link_model.user)
        except UserSocialAccounts.DoesNotExist:
            logger.debug(f"Social Link({social_link.provider_name}: {social_link.social_id})에 해당하는 사용자를 찾을 수 없습니다.")
            return None
        except DatabaseError as e:
            logger.error(f"Social Link로 사용자 조회 중 데이터베이스 오류 발생: {e}", exc_info=True)
            raise Exception("데이터베이스 조회 중 오류가 발생했습니다.")