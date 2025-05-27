import unittest
from apps.account.domain.value_objects.nickname import NickName

class TestNickName(unittest.TestCase):

    def test_create_valid_nickname(self):
        # 계약: 유효한 길이와 형식의 문자열로 NickName 객체를 성공적으로 생성할 수 있어야 한다.
        valid_names = ["테스트닉", "닉네임123", "Nick123", "ab"]
        for name in valid_names:
            with self.subTest(name=name):
                nickname_vo = NickName(name)
                self.assertIsInstance(nickname_vo, NickName)
                self.assertEqual(nickname_vo.name, name)

    def test_create_nickname_with_empty_string_raises_value_error(self):
        # 계약: 비어있는 문자열로 Nickname 객체 생성을 시도하면 ValueError가 발생해야 한다.
        # 계약: 오류 메시지는 "닉네임은 비어있을 수 없습니다." 이어야 한다.
        with self.assertRaisesRegex(ValueError, "닉네임은 비어있을 수 없습니다."):
            NickName("")

    def test_create_nickname_with_none_raises_value_error(self):
        # 계약: None 값으로 Nickname 객체 생성을 시도하면 ValueError가 발생해야 한다.
        # 계약: 오류 메시지는 "닉네임은 비어있을 수 없습니다." 이어야 한다.
        with self.assertRaisesRegex(ValueError, "닉네임은 비어있을 수 없습니다."):
            NickName(None)  # type: ignore

    def test_create_nickname_too_short_raises_value_error(self):
        # 계약: 최소 길이(2자)보다 짧은 닉네임으로 객체 생성을 시도하면 ValueError가 발생해야 한다.
        # 계약: 오류 메시지는 "닉네임은 2자 이상 15자 이하이어야 합니다." 이어야 한다.
        with self.assertRaisesRegex(ValueError, "닉네임은 2자 이상 15자 이하이어야 합니다."):
            NickName("닉")  # 1자

    def test_create_nickname_too_long_raises_value_error(self):
        # 계약: 최대 길이(15자)를 초과하는 닉네임으로 객체 생성을 시도하면 ValueError가 발생해야 한다.
        # 계약: 오류 메시지는 "닉네임은 2자 이상 15자 이하이어야 합니다." 이어야 한다.
        with self.assertRaisesRegex(ValueError, "닉네임은 2자 이상 15자 이하이어야 합니다."):
            NickName("a" * 16)  # 16자

    def test_create_nickname_at_min_length(self):
        # 계약: 최소 길이(2자)의 닉네임으로 객체가 성공적으로 생성되어야 한다.
        name = "ab"
        try:
            nickname_vo = NickName(name)
            self.assertEqual(nickname_vo.name, name)
        except ValueError:
            self.fail("최소 길이 2자 닉네임 생성에 실패했습니다.")

    def test_create_nickname_at_max_length(self):
        # 계약: 최대 길이(15자)의 닉네임으로 객체가 성공적으로 생성되어야 한다.
        name = "a" * 15
        try:
            nickname_vo = NickName(name)
            self.assertEqual(nickname_vo.name, name)
        except ValueError:
            self.fail("최대 길이 15자 닉네임 생성에 실패했습니다.")

    def test_nickname_equality_based_on_name(self):
        # 계약: 두 Nickname 객체는 name 속성 값이 같으면 동등한 것으로 간주되어야 한다.
        nick1 = NickName("같은닉네임")
        nick2 = NickName("같은닉네임")
        nick3 = NickName("다른닉네임")

        self.assertEqual(nick1, nick2)
        self.assertTrue(nick1 == nick2)
        self.assertNotEqual(nick1, nick3)
        self.assertFalse(nick1 == nick3)

    def test_nickname_equality_with_other_types(self):
        # 계약: Nickname 객체는 다른 타입의 객체와 동등하지 않아야 한다.
        nick1 = NickName("테스트닉네임")
        self.assertNotEqual(nick1, "테스트닉네임")  # 문자열과 비교
        self.assertNotEqual(nick1, None)

    def test_nickname_hash_consistency(self):
        # 계약: 동등한 Nickname 객체는 동일한 해시 값을 가져야 한다.
        nick1 = NickName("해시테스트")
        nick2 = NickName("해시테스트")
        self.assertEqual(hash(nick1), hash(nick2))

    def test_nickname_string_representation(self):
        # 계약: Nickname 객체의 문자열 표현은 닉네임 문자열 자체여야 한다.
        name_str = "문자열표현"
        nickname_vo = NickName(name_str)
        self.assertEqual(str(nickname_vo), name_str)


if __name__ == '__main__':
    unittest.main()
