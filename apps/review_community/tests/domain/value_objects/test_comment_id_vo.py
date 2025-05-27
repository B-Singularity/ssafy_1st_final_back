# 파일 경로: apps/review_community/tests/domain/value_objects/test_comment_id_vo.py
import unittest
import uuid
import re

from apps.review_community.domain.value_objects.comment_id_vo import CommentIdVO

class TestCommentIdValueObject(unittest.TestCase):

    def test_create_valid_uuid_string(self):
        # 계약: 유효한 UUID 문자열로 CommentIdVO를 성공적으로 생성할 수 있어야 한다.
        # 계약: 생성된 객체의 value 속성은 입력된 UUID 문자열과 같아야 한다.
        valid_uuid_str = str(uuid.uuid4())
        comment_id_vo = CommentIdVO(valid_uuid_str)
        self.assertIsInstance(comment_id_vo, CommentIdVO)
        self.assertEqual(comment_id_vo.value, valid_uuid_str)

    def test_generate_new_id_with_classmethod(self):
        # 계약: generate 클래스 메서드는 새로운 유효한 CommentIdVO 인스턴스를 생성해야 한다.
        # 계약: 생성된 ID의 value는 UUID 형식이어야 한다.
        # 계약: 연속으로 생성된 ID들은 서로 다른 값을 가져야 한다.
        id_vo1 = CommentIdVO.generate()
        id_vo2 = CommentIdVO.generate()

        self.assertIsInstance(id_vo1, CommentIdVO)
        self.assertIsInstance(id_vo2, CommentIdVO)
        
        try:
            uuid.UUID(id_vo1.value, version=4)
            uuid.UUID(id_vo2.value, version=4)
        except ValueError:
            self.fail("generate() 메서드가 유효한 UUID 형식의 ID를 생성하지 못했습니다.")
            
        self.assertNotEqual(id_vo1.value, id_vo2.value)

    def test_create_with_empty_string_raises_value_error(self):
        # 계약: 비어있는 문자열로 CommentIdVO 생성을 시도하면 ValueError가 발생해야 한다.
        # 계약: 오류 메시지는 "댓글 ID 값은 비어있을 수 없습니다." 이어야 한다.
        with self.assertRaisesRegex(ValueError, "댓글 ID 값은 비어있을 수 없습니다."):
            CommentIdVO("")

    def test_create_with_none_value_raises_value_error(self):
        # 계약: None 값으로 CommentIdVO 생성을 시도하면 ValueError가 발생해야 한다.
        # 계약: 오류 메시지는 "댓글 ID 값은 비어있을 수 없습니다." 이어야 한다.
        with self.assertRaisesRegex(ValueError, "댓글 ID 값은 비어있을 수 없습니다."):
            CommentIdVO(None)

    def test_create_with_non_string_type_raises_type_error(self):
        # 계약: ID 값이 문자열이 아닐 경우 TypeError가 발생해야 한다.
        # 계약: 오류 메시지는 "댓글 ID 값은 문자열이어야 합니다." 이어야 한다.
        with self.assertRaisesRegex(TypeError, "댓글 ID 값은 문자열이어야 합니다."):
            CommentIdVO(12345)

    def test_create_with_invalid_uuid_format_raises_value_error(self):
        # 계약: 유효하지 않은 UUID 형식의 문자열로 CommentIdVO 생성을 시도하면 ValueError가 발생해야 한다.
        invalid_uuids_and_messages = [
            ("not-a-uuid", "유효하지 않은 UUID 문자열 형식입니다: 'not-a-uuid'"),
            ("123e4567-e89b-12d3-a456-42661417400", "유효하지 않은 UUID 문자열 형식입니다: '123e4567-e89b-12d3-a456-42661417400'"),
            ("123e4567-e89b-12d3-a456-4266141740000", "유효하지 않은 UUID 문자열 형식입니다: '123e4567-e89b-12d3-a456-4266141740000'")
        ]
        version_1_uuid_str = str(uuid.uuid1())
        # CommentIdVO에서 버전 불일치 시 발생하는 특정 메시지를 기대
        invalid_uuids_and_messages.append((version_1_uuid_str, "댓글 ID는 UUID 버전 4 형식이어야 합니다."))

        for invalid_uuid, expected_message in invalid_uuids_and_messages:
            with self.subTest(invalid_uuid=invalid_uuid):
                # 기대하는 오류 메시지를 실제 발생하는 메시지에 맞게 수정
                with self.assertRaisesRegex(ValueError, re.escape(expected_message)): # re.escape 사용
                    CommentIdVO(invalid_uuid)

    def test_equality_comparison(self):
        # 계약: 두 CommentIdVO 객체는 내부 value 속성 값이 같으면 동등한 것으로 간주되어야 한다.
        uuid_val = str(uuid.uuid4())
        id1 = CommentIdVO(uuid_val)
        id2 = CommentIdVO(uuid_val)
        id3 = CommentIdVO(str(uuid.uuid4()))

        self.assertEqual(id1, id2)
        self.assertTrue(id1 == id2)
        self.assertNotEqual(id1, id3)
        self.assertFalse(id1 == id3)

    def test_equality_comparison_with_other_types(self):
        # 계약: CommentIdVO 객체는 다른 타입의 객체와 동등하지 않아야 한다.
        uuid_val = str(uuid.uuid4())
        id1 = CommentIdVO(uuid_val)
        self.assertNotEqual(id1, uuid_val) 
        self.assertNotEqual(id1, None)

    def test_hash_consistency(self):
        # 계약: 동등한 CommentIdVO 객체는 동일한 해시 값을 가져야 한다.
        uuid_val = str(uuid.uuid4())
        id1 = CommentIdVO(uuid_val)
        id2 = CommentIdVO(uuid_val)
        self.assertEqual(hash(id1), hash(id2))

    def test_string_representation(self):
        # 계약: CommentIdVO 객체의 문자열 표현은 내부 UUID 문자열 값이어야 한다.
        uuid_val = str(uuid.uuid4())
        id_vo = CommentIdVO(uuid_val)
        self.assertEqual(str(id_vo), uuid_val)

if __name__ == '__main__':
    unittest.main()