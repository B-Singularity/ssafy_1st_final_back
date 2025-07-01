import pytest
from unittest.mock import MagicMock

from apps.account.infrastructure.token_services import SimpleJwtTokenService


# 계약: 토큰 발급 시, SimpleJwtTokenService는 올바른 User 모델을 찾아 토큰을 생성해야 한다.
def test_issue_for_user(mocker):
    mock_user = MagicMock()
    mock_get_user = mocker.patch('apps.account.infrastructure.token_services.Users.objects.get', return_value=mock_user)

    mock_access_token = MagicMock()
    mock_access_token.__str__.return_value = "fake_access_token_string"

    mock_refresh_token = MagicMock()
    mock_refresh_token.__str__.return_value = "fake_refresh_token_string"
    type(mock_refresh_token).access_token = mock_access_token

    mock_for_user = mocker.patch('apps.account.infrastructure.token_services.RefreshToken.for_user', return_value=mock_refresh_token)
    token_service = SimpleJwtTokenService()

    result_tokens = token_service.issue_for_user(user_account_id=123)

    mock_for_user.assert_called_once_with(mock_user)
    assert result_tokens["access"] == "fake_access_token_string"
    assert result_tokens["refresh"] == "fake_refresh_token_string"


# 계약: 로그아웃(블랙리스트) 시, SimpleJwtTokenService는 RefreshToken 객체를 생성하고 blacklist 메서드를 호출해야 한다.
def test_blacklist_token_successfully(mocker):
    # --- 1. 준비 (Arrange) ---

    # RefreshToken 클래스 자체를 Mocking합니다.
    mock_refresh_token_class = mocker.patch('apps.account.infrastructure.token_services.RefreshToken')

    # 생성된 Mock 클래스의 인스턴스에서 blacklist 메서드를 가져옵니다.
    mock_blacklist_method = mock_refresh_token_class.return_value.blacklist

    token_service = SimpleJwtTokenService()
    fake_refresh_token = "any_refresh_token_string"

    # --- 2. 실행 (Act) ---
    token_service.blacklist(fake_refresh_token)

    # --- 3. 검증 (Assert) ---

    # RefreshToken 클래스가 올바른 토큰 문자열로 초기화되었는지 확인합니다.
    mock_refresh_token_class.assert_called_once_with(fake_refresh_token)

    # blacklist 메서드가 호출되었는지 확인합니다.
    mock_blacklist_method.assert_called_once()