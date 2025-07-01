import pytest
from datetime import datetime

from src.apps.account.application.services import (
    UserAuthAppService,
    UserProfileAppService,
    UserAccountDeactivationAppService
)
from src.apps.account.application.ports.social_verifier import SocialUserInfo
from src.apps.account.domain.aggregates.user_account import UserAccount
from src.apps.account.domain.value_objects.email import Email
from src.apps.account.domain.value_objects.nickname import NickName
from src.apps.account.application.dtos import SocialLoginRequestDto


# ==================================
# UserAuthAppService 테스트
# ==================================
@pytest.mark.django_db
class TestUserAuthAppService:

    @pytest.fixture
    def auth_service_components(self, mocker):
        # mocker.patch('django.db.transaction.atomic') # 이 라인을 삭제합니다.

        mock_repo = mocker.MagicMock()
        mock_google_verifier_factory = mocker.MagicMock()
        mock_token_service = mocker.MagicMock()

        verifier_map = {"google": mock_google_verifier_factory}

        service = UserAuthAppService(
            user_account_repository=mock_repo,
            social_verifier_map=verifier_map,
            token_service=mock_token_service
        )
        return {
            "service": service, "repository": mock_repo,
            "google_verifier_factory": mock_google_verifier_factory, "token_service": mock_token_service
        }

    def test_register_for_completely_new_user_should_succeed(self, auth_service_components):
        service = auth_service_components["service"]
        mock_repo = auth_service_components["repository"]
        mock_verifier_factory = auth_service_components["google_verifier_factory"]
        mock_token = auth_service_components["token_service"]

        mock_verifier = mock_verifier_factory.return_value

        request_dto = SocialLoginRequestDto("google", "token", "new@email.com", "새유저")

        mock_repo.find_by_social_link.return_value = None
        mock_repo.find_by_email.return_value = None
        mock_repo.find_by_nickname.return_value = None
        mock_verifier.verify.return_value = SocialUserInfo("google_id", "new@email.com", "Google Nick")
        mock_repo.save.side_effect = lambda user_account: UserAccount(1, user_account.email, user_account.nickname,
                                                                      user_account.social_links, datetime.now())
        mock_token.issue_for_user.return_value = {"access": "a", "refresh": "b"}

        result = service.login_or_register(request_dto)

        mock_repo.save.assert_called_once()
        saved_user_arg = mock_repo.save.call_args[0][0]
        assert saved_user_arg.nickname.name == "새유저"
        assert result.is_new_user is True


# ==================================
# UserProfileAppService 테스트
# ==================================
@pytest.mark.django_db
class TestUserProfileAppService:

    @pytest.fixture
    def profile_service_components(self, mocker):
        # mocker.patch('django.db.transaction.atomic') # 이 라인을 삭제합니다.
        mock_repo = mocker.MagicMock()
        service = UserProfileAppService(user_account_repository=mock_repo)
        return {"service": service, "repository": mock_repo}

    def test_get_user_profile_when_user_exists(self, profile_service_components):
        service = profile_service_components["service"]
        mock_repo = profile_service_components["repository"]

        user_domain = UserAccount(1, Email("test@test.com"), NickName("테스트"), [], datetime.now())
        mock_repo.find_by_id.return_value = user_domain

        result_dto = service.get_user_profile(1)

        mock_repo.find_by_id.assert_called_once_with(1)
        assert result_dto is not None
        assert result_dto.nickname== "테스트"


# ==================================
# UserAccountDeactivationAppService 테스트
# ==================================
@pytest.mark.django_db
class TestUserAccountDeactivationAppService:

    def test_deactivate_account_should_call_repository_delete(self, mocker):
        # mocker.patch('django.db.transaction.atomic') # 이 라인을 삭제합니다.
        mock_repo = mocker.MagicMock()
        service = UserAccountDeactivationAppService(user_account_repository=mock_repo)

        service.deactivate_account(123)

        mock_repo.delete.assert_called_once_with(123)