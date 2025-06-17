import pytest
from apps.account.domain.value_objects.nickname import NickName

# 계약: 유효한 닉네임으로 객체를 성공적으로 생성할 수 있어야 한다.
@pytest.mark.parametrize("valid_name", ["테스트닉", "닉네임123", "Nick123", "ab", "a" * 15])
def test_create_valid_nickname(valid_name):
    nickname_vo = NickName(valid_name)
    assert nickname_vo.name == valid_name

# 계약: 유효하지 않은 닉네임으로 객체 생성을 시도하면 ValueError가 발생해야 한다.
@pytest.mark.parametrize("invalid_name, error_message", [
    ("", "닉네임은 비어있을 수 없습니다."),
    (None, "닉네임은 비어있을 수 없습니다."),
    ("닉", "닉네임은 2자 이상 15자 이하이어야 합니다."),
    ("a" * 16, "닉네임은 2자 이상 15자 이하이어야 합니다."),
])
def test_create_invalid_nickname_raises_error(invalid_name, error_message):
    with pytest.raises(ValueError, match=error_message):
        NickName(invalid_name)

# 계약: 두 Nickname 객체는 name 속성 값이 같으면 동등한 것으로 간주되어야 한다.
def test_nickname_equality():
    nick1 = NickName("같은닉네임")
    nick2 = NickName("같은닉네임")
    nick3 = NickName("다른닉네임")
    assert nick1 == nick2
    assert nick1 != nick3