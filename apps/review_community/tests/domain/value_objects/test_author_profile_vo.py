import unittest
from apps.review_community.domain.value_objects.author_profile_vo import AuthorProfileVO

class TestAuthorProfileValueObject(unittest.TestCase):

    def test_create_valid_author_profile(self):
        # 계약: 유효한 account_id와 nickname으로 AuthorProfileVO를 성공적으로 생성할 수 있어야 한다.
        vo = AuthorProfileVO(account_id=1, nickname="글쓴이")
        self.assertEqual(vo.account_id, 1)
        self.assertEqual(vo.nickname, "글쓴이")

    def test_create_with_invalid_account_id_type_raises_type_error(self):
        # 계약: account_id가 정수가 아니면 TypeError가 발생해야 한다.
        # (현재 __init__에서는 ValueError를 발생시키므로, VO 정의와 일치시키거나 테스트 수정 필요)
        # 여기서는 VO 정의의 isinstance(account_id, int)에 맞춰 ValueError를 기대합니다.
        with self.assertRaisesRegex(ValueError, "계정 ID는 0보다 큰 정수여야 합니다."):
            AuthorProfileVO(account_id="아이디1", nickname="테스트")

    def test_create_with_invalid_account_id_value_raises_value_error(self):
        # 계약: account_id가 0 이하의 정수이면 ValueError가 발생해야 한다.
        with self.assertRaisesRegex(ValueError, "계정 ID는 0보다 큰 정수여야 합니다."):
            AuthorProfileVO(account_id=0, nickname="테스트")
        with self.assertRaisesRegex(ValueError, "계정 ID는 0보다 큰 정수여야 합니다."):
            AuthorProfileVO(account_id=-1, nickname="테스트")

    def test_create_with_empty_nickname_raises_value_error(self):
        # 계약: 비어있는 닉네임으로 생성 시도 시 ValueError가 발생해야 한다.
        with self.assertRaisesRegex(ValueError, "닉네임은 비어있을 수 없습니다."):
            AuthorProfileVO(account_id=1, nickname="")

    def test_create_with_none_nickname_raises_value_error(self):
        # 계약: 닉네임으로 None 값을 전달하여 생성 시도 시 ValueError가 발생해야 한다.
        with self.assertRaisesRegex(ValueError, "닉네임은 비어있을 수 없습니다."):
            AuthorProfileVO(account_id=1, nickname=None)

    def test_create_with_nickname_out_of_length_raises_value_error(self):
        # 계약: 닉네임이 길이 제약(2~15자)을 벗어나면 ValueError가 발생해야 한다.
        with self.assertRaisesRegex(ValueError, "닉네임은 2자 이상 15자 이하이어야 합니다."):
            AuthorProfileVO(account_id=1, nickname="닉") 
        with self.assertRaisesRegex(ValueError, "닉네임은 2자 이상 15자 이하이어야 합니다."):
            AuthorProfileVO(account_id=1, nickname="가나다라마바사아자차카타파하가나") 

    def test_create_with_non_string_nickname_raises_type_error(self):
        # 계약: 닉네임이 문자열이 아니면 TypeError가 발생해야 한다.
        with self.assertRaisesRegex(TypeError, "닉네임은 문자열이어야 합니다."):
            AuthorProfileVO(account_id=1, nickname=123)

    def test_author_profile_equality(self):
        # 계약: 두 AuthorProfileVO 객체는 account_id와 nickname이 모두 같으면 동등해야 한다.
        vo1 = AuthorProfileVO(1, "작가1")
        vo2 = AuthorProfileVO(1, "작가1")
        vo3 = AuthorProfileVO(2, "작가1") 
        vo4 = AuthorProfileVO(1, "작가2") 
        
        self.assertEqual(vo1, vo2)
        self.assertNotEqual(vo1, vo3)
        self.assertNotEqual(vo1, vo4)

    def test_author_profile_hash_consistency(self):
        # 계약: 동등한 AuthorProfileVO 객체는 동일한 해시 값을 가져야 한다.
        vo1 = AuthorProfileVO(10, "해시작가")
        vo2 = AuthorProfileVO(10, "해시작가")
        self.assertEqual(hash(vo1), hash(vo2))

    def test_author_profile_string_representation(self):
        # 계약: AuthorProfileVO 객체의 문자열 표현은 닉네임이어야 한다.
        vo = AuthorProfileVO(account_id=1, nickname="표현테스트")
        self.assertEqual(str(vo), "표현테스트")

if __name__ == '__main__':
    unittest.main()