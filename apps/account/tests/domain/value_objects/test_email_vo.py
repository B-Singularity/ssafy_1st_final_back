import unittest
from apps.account.domain.value_objects.email import Email

class TestEmail(unittest.TestCase):
    # 계약: 유효한 형식의 이메일 주소로 Email 객체를 성공적으로 생성할 수 있어야 한다.
    def test_create_valid_email(self):
        valid_address = "test@example.com"
        email_vo = Email(valid_address)
        self.assertIsInstance(email_vo, Email)
        self.assertEqual(email_vo.address, valid_address)

    # 계약: 비어있는 문자열로 Email 객체 생성을 시도하면 ValueError가 발생해야 한다.
    # 계약: 오류 메시지는 "이메일 주소는 비어있을 수 없습니다." 이어야 한다.
    def test_create_empty_email(self):
        with self.assertRaisesRegex(ValueError, "이메일 주소는 비어있을 수 없습니다."):
            Email("")
    # 계약: None 값으로 Email 객체 생성을 시도하면 ValueError가 발생해야 한다.
    # 계약: 오류 메시지는 "이메일 주소는 비어있을 수 없습니다." 이어야 한다.
    def test_create_email_with_none_raises_value_error(self):
        with self.assertRaisesRegex(ValueError, "이메일 주소는 비어있을 수 없습니다."):
            Email(None)

    # 계약: 유효하지 않은 형식의 이메일 주소로 Email 객체 생성을 시도하면 ValueError가 발생해야 한다.
    # 계약: 오류 메시지는 "유효하지 않은 이메일 형식입니다." 이어야 한다.
    def test_create_email_with_invalid_format_raises_value_error(self):
        invalid_emails = [
            "testexample.com",
            "test@examplecom",
            "@example.com",
            "test@",
            "test@.com"
        ]
        for invalid_email in invalid_emails:
            with self.subTest(invalid_email=invalid_email):
                with self.assertRaisesRegex(ValueError, "유효하지 않은 이메일 형식입니다."):
                    Email(invalid_email)

    # 계약: 최대 길이(254자)를 초과하는 이메일 주소로 Email 객체 생성을 시도하면 ValueError가 발생해야 한다.
    # 계약: 오류 메시지는 "이메일 주소는 최대 254자까지 가능합니다." 이어야 한다.
    def test_create_email_exceeding_max_length_raises_value_error(self):
        invalid_long_email = ("a" * 249) + "@b.com"  # 249 + 1 + 1 + 1 + 3 = 255자
        with self.assertRaisesRegex(ValueError, "이메일 주소는 최대 254자까지 가능합니다."):
            Email(invalid_long_email)

        valid_long_email_at_max = ("a" * 248) + "@b.com"  # 248 + 1 + 1 + 1 + 3 = 254자
        try:
            Email(valid_long_email_at_max)
        except ValueError:
            self.fail("최대 길이 254자 이메일 생성에 실패했습니다.")

    # 계약: 두 Email 객체는 address 속성 값이 같으면 동등한 것으로 간주되어야 한다.
    def test_email_equality_based_on_address(self):
        email1 = Email("test@example.com")
        email2 = Email("test@example.com")
        email3 = Email("another@example.com")

        self.assertEqual(email1, email2) # email1 == email2
        self.assertTrue(email1 == email2)
        self.assertNotEqual(email1, email3) # email1 != email3
        self.assertFalse(email1 == email3)

    # 계약: Email 객체는 다른 타입의 객체와 동등하지 않아야 한다.
    def test_email_equality_with_other_types(self):
        email1 = Email("test@example.com")
        self.assertNotEqual(email1, "test@example.com")
        self.assertNotEqual(email1, None)

    # 계약: 동등한 Email 객체는 동일한 해시 값을 가져야 한다.
    def test_email_hash_consistency(self):
        email1 = Email("test@example.com")
        email2 = Email("test@example.com")
        self.assertEqual(hash(email1), hash(email2))

    # 계약: Email 객체의 문자열 표현은 이메일 주소 자체여야 한다.
    def test_email_string_representation(self):
        email_address = "test@example.com"
        email_vo = Email(email_address)
        self.assertEqual(str(email_vo), email_address)

if __name__ == '__main__':
    unittest.main()