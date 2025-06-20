import pytest
from src.apps.account.domain.value_objects.email import Email

# 계약: 유효한 형식의 이메일 주소로 Email 객체를 성공적으로 생성할 수 있어야 한다.
def test_create_valid_email():
    valid_address = "test@example.com"
    email_vo = Email(valid_address)
    assert isinstance(email_vo, Email)
    assert email_vo.address == valid_address

# 계약: 비어있거나 None 값으로 Email 객체 생성을 시도하면 ValueError가 발생해야 한다.
@pytest.mark.parametrize("empty_input", ["", None])
def test_create_email_with_empty_or_none_raises_error(empty_input):
    with pytest.raises(ValueError, match="이메일 주소는 비어있을 수 없습니다."):
        Email(empty_input)

# 계약: 유효하지 않은 형식의 이메일 주소로 Email 객체 생성을 시도하면 ValueError가 발생해야 한다.
@pytest.mark.parametrize("invalid_email", [
    "testexample.com",
    "test@examplecom",
    "@example.com",
    "test@",
    "test@.com"
])
def test_create_email_with_invalid_format_raises_error(invalid_email):
    with pytest.raises(ValueError, match="유효하지 않은 이메일 형식입니다."):
        Email(invalid_email)

# 계약: 최대 길이(254자)를 초과하는 이메일 주소로 Email 객체 생성을 시도하면 ValueError가 발생해야 한다.
def test_create_email_exceeding_max_length_raises_error():
    invalid_long_email = ("a" * 249) + "@b.com"  # 255자
    with pytest.raises(ValueError, match="이메일 주소는 최대 254자까지 가능합니다."):
        Email(invalid_long_email)

# 계약: 최대 길이(254자)의 이메일 주소로 객체가 성공적으로 생성되어야 한다.
def test_create_email_at_max_length():
    valid_long_email_at_max = ("a" * 248) + "@b.com"  # 254자
    try:
        Email(valid_long_email_at_max)
    except ValueError:
        pytest.fail("최대 길이 254자 이메일 생성에 실패했습니다.")

# 계약: 두 Email 객체는 address 속성 값이 같으면 동등한 것으로 간주되어야 한다.
def test_email_equality_based_on_address():
    email1 = Email("test@example.com")
    email2 = Email("test@example.com")
    email3 = Email("another@example.com")

    assert email1 == email2
    assert email1 != email3

# 계약: Email 객체는 다른 타입의 객체와 동등하지 않아야 한다.
def test_email_equality_with_other_types():
    email1 = Email("test@example.com")
    assert email1 != "test@example.com"
    assert email1 != None

# 계약: 동등한 Email 객체는 동일한 해시 값을 가져야 한다.
def test_email_hash_consistency():
    email1 = Email("test@example.com")
    email2 = Email("test@example.com")
    assert hash(email1) == hash(email2)

# 계약: Email 객체의 문자열 표현은 이메일 주소 자체여야 한다.
def test_email_string_representation():
    email_address = "test@example.com"
    email_vo = Email(email_address)
    assert str(email_vo) == email_address