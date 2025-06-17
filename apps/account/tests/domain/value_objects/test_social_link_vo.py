import pytest
from apps.account.domain.value_objects.social_link import SocialLink

# 계약: 유효한 provider와 social_id로 SocialLink 객체를 성공적으로 생성할 수 있어야 한다.
def test_create_valid_social_link():
    social_link = SocialLink(provider_name="google", social_id="user123")
    assert social_link.provider_name == "google"
    assert social_link.social_id == "user123"

# 계약: 유효하지 않은 파라미터로 객체 생성을 시도하면 적절한 예외가 발생해야 한다.
@pytest.mark.parametrize("provider, social_id, error_type, error_message", [
    ("facebook", "user123", ValueError, "지원하지 않는 소셜 정보 제공자입니다: facebook"),
    ("google", "", ValueError, "소셜 ID는 비어있을 수 없습니다."),
    ("google", None, ValueError, "소셜 ID는 비어있을 수 없습니다."),
    (123, "user123", TypeError, "provider_name은 문자열이어야 합니다."),
    ("google", 123, TypeError, "social_id는 문자열이어야 합니다."),
])
def test_create_invalid_social_link_raises_error(provider, social_id, error_type, error_message):
    with pytest.raises(error_type, match=error_message):
        SocialLink(provider_name=provider, social_id=social_id)

# 계약: 두 SocialLink 객체는 속성 값이 모두 같으면 동등한 것으로 간주되어야 한다.
def test_social_link_equality():
    link1 = SocialLink(provider_name="google", social_id="user123")
    link2 = SocialLink(provider_name="google", social_id="user123")
    link3 = SocialLink(provider_name="google", social_id="user456")
    assert link1 == link2
    assert link1 != link3