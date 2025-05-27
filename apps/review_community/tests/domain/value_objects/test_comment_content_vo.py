import unittest
from apps.review_community.domain.value_objects.comment_content_vo import CommentContentVO

class TestCommentContentValueObject(unittest.TestCase):

    def test_create_valid_comment_content(self):
        # 계약: 유효한 문자열로 CommentContentVO를 성공적으로 생성할 수 있어야 한다.
        content = "이 영화 정말 재미있어요!"
        vo = CommentContentVO(content)
        self.assertIsInstance(vo, CommentContentVO)
        self.assertEqual(vo.text, content)

    def test_create_with_whitespace_stripping(self):
        # 계약: 내용 생성 시 앞뒤 공백은 제거되어야 한다.
        content_with_space = "  공백 제거 테스트  "
        expected_content = "공백 제거 테스트"
        vo = CommentContentVO(content_with_space)
        self.assertEqual(vo.text, expected_content)

    def test_create_with_empty_string_after_strip_raises_value_error(self):
        # 계약: 공백만 있는 문자열(strip 후 빈 문자열)로 생성 시도 시 ValueError가 발생해야 한다.
        with self.assertRaisesRegex(ValueError, "댓글 내용은 비어있을 수 없습니다."):
            CommentContentVO("   ")

    def test_create_with_none_value_raises_value_error(self):
        # 계약: None 값으로 생성 시도 시 ValueError가 발생해야 한다.
        with self.assertRaisesRegex(ValueError, "댓글 내용은 None일 수 없습니다."):
            CommentContentVO(None)

    def test_create_with_non_string_type_raises_type_error(self):
        # 계약: 내용이 문자열이 아닐 경우 TypeError가 발생해야 한다.
        with self.assertRaisesRegex(TypeError, "댓글 내용은 문자열이어야 합니다."):
            CommentContentVO(12345)

    def test_create_with_content_too_long_raises_value_error(self):
        # 계약: 내용이 최대 길이(500자)를 초과하면 ValueError가 발생해야 한다.
        long_content = "가" * 501
        with self.assertRaisesRegex(ValueError, "댓글 내용은 최대 500자까지 가능합니다."):
            CommentContentVO(long_content)

    def test_create_with_content_at_max_length(self):
        # 계약: 최대 길이(500자)의 내용으로 객체가 성공적으로 생성되어야 한다.
        content = "나" * 500
        try:
            vo = CommentContentVO(content)
            self.assertEqual(vo.text, content)
        except ValueError:
            self.fail("최대 길이 500자 댓글 내용 생성에 실패했습니다.")

    def test_equality(self):
        # 계약: 두 CommentContentVO 객체는 text 속성 값이 같으면 동등해야 한다.
        content = "동일한 내용입니다."
        vo1 = CommentContentVO(content)
        vo2 = CommentContentVO(content)
        vo3 = CommentContentVO("다른 내용입니다.")
        self.assertEqual(vo1, vo2)
        self.assertNotEqual(vo1, vo3)

    def test_hash_consistency(self):
        # 계약: 동등한 CommentContentVO 객체는 동일한 해시 값을 가져야 한다.
        content = "해시 테스트용 내용"
        vo1 = CommentContentVO(content)
        vo2 = CommentContentVO(content)
        self.assertEqual(hash(vo1), hash(vo2))

    def test_string_representation(self):
        # 계약: CommentContentVO 객체의 문자열 표현은 댓글 내용 자체여야 한다.
        content = "이것이 댓글 내용입니다."
        vo = CommentContentVO(content)
        self.assertEqual(str(vo), content)

if __name__ == '__main__':
    unittest.main()