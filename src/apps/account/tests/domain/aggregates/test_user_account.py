import pytest
from datetime import datetime, timedelta

from apps.account.domain.aggregates.user_account import UserAccount
from apps.account.domain.value_objects.email import Email
from apps.account.domain.value_objects.nickname import NickName
from apps.account.domain.value_objects.social_link import SocialLink

@pytest.fixture
def user_account():
    return UserAccount(
        account_id=1,
        email=Email("test@example.com"),
        nickname=NickName("기존닉네임"),
        social_links=[SocialLink("google", "google_id_123")],
        created_at=datetime.now(),
        last_login_at=datetime.now()
    )

class TestUserAccountAggregate:
    # 계약: record_login 호출 시, last_login_at 속성이 올바르게 갱신되어야 한다.
    def test_record_login_updates_last_login_at(self, user_account):
        initial_login_time = user_account.last_login_at
        new_login_time = datetime.now() + timedelta(minutes=10)

        user_account.record_login(new_login_time)

        assert user_account.last_login_at == new_login_time
        assert user_account.last_login_at != initial_login_time

    # 계약: add_social_link 호출 시, 새로운 소설 링크가 리스트에 추가되어야 한다.
    def test_add_new_social_link(self, user_account):
        initial_link_count = len(user_account.social_links)
        new_link = SocialLink("kakao", "kakao_id_456")

        user_account.add_social_link(new_link)

        assert len(user_account.social_links) == initial_link_count + 1
        assert new_link in user_account.social_links

    # 계약: 이미 존재하는 소셜 링크를 add_social_link로 추가해도, 리스트에 변화가 없어야 한다.
    def test_add_existing_social_link_does_not_duplicate(self, user_account):
        existing_link = SocialLink("google", "google_id_123")
        initial_link_count = len(user_account.social_links)

        user_account.add_social_link(existing_link)

        assert len(user_account.social_links) == initial_link_count

    # 계약: 닉네임 유일성 검사를 통과하면, 닉네임이 성공적으로 변경되어야 한다.
    def test_update_nickname_successfully_when_unique(self, user_account):
        new_nickname = NickName("새로운닉네임")
        unique_checker = lambda nickname, account_id: True

        user_account.update_nickname(new_nickname, unique_checker)

        assert user_account.nickname == new_nickname

    # 계약: 닉네임 유일성 검사를 통과하지 못하면, ValueError가 발생해야 한다.
    def test_update_nickname_fails_when_not_unique(self, user_account):
        new_nickname = NickName("중복된닉네임")
        not_unique_checker = lambda nickname, account_id: False

        with pytest.raises(ValueError, match=f"닉네임 '{new_nickname.name}'은 이미 사용 중입니다." ):
            user_account.update_nickname(new_nickname, not_unique_checker)

        assert user_account.nickname.name == "기존닉네임"


    # 계약: 현재와 동일한 닉네임으로 변경을 시도하면, 아무 일도 일어나지 않아야 한다.
    def test_update_nickname_with_same_name_does_nothing(self, user_account, mocker):
        same_nickname = NickName("기존닉네임")
        mock_checker = mocker.MagicMock()

        user_account.update_nickname(same_nickname, mock_checker)

        assert user_account.nickname.name == "기존닉네임"
        mock_checker.assert_not_called()