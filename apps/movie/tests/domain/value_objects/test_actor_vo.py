import unittest
from apps.movie.domain.value_objects.actor_vo import ActorVO

class TestActorValueObject(unittest.TestCase):

    def test_create_valid_actor_all_fields(self):
        # 계약: 모든 필드가 유효한 값으로 ActorVO를 성공적으로 생성할 수 있어야 한다.
        vo = ActorVO(name="톰 행크스", role_name="포레스트 검프", external_id="tmdb_actor_123")
        self.assertEqual(vo.name, "톰 행크스")
        self.assertEqual(vo.role_name, "포레스트 검프")
        self.assertEqual(vo.external_id, "tmdb_actor_123")

    def test_create_valid_actor_name_only(self):
        # 계약: 필수 필드인 이름만으로 ActorVO를 성공적으로 생성할 수 있어야 한다.
        vo = ActorVO(name="송강호")
        self.assertEqual(vo.name, "송강호")
        self.assertIsNone(vo.role_name)
        self.assertIsNone(vo.external_id)

    def test_create_valid_actor_name_and_role(self):
        # 계약: 이름과 배역명으로 ActorVO를 성공적으로 생성할 수 있어야 한다.
        vo = ActorVO(name="최민식", role_name="이순신")
        self.assertEqual(vo.name, "최민식")
        self.assertEqual(vo.role_name, "이순신")
        self.assertIsNone(vo.external_id)

    def test_create_with_empty_name_raises_value_error(self):
        # 계약: 비어있는 이름으로 생성 시도 시 ValueError가 발생해야 한다.
        with self.assertRaisesRegex(ValueError, "배우 이름은 비어있을 수 없습니다."):
            ActorVO(name="")

    def test_create_with_name_too_long_raises_value_error(self):
        # 계약: 이름이 최대 길이(100자)를 초과하면 ValueError가 발생해야 한다.
        with self.assertRaisesRegex(ValueError, "배우 이름은 유효한 문자열이어야 하며 최대 100자입니다."):
            ActorVO(name="가" * 101)

    def test_create_with_role_name_too_long_raises_value_error(self):
        # 계약: 배역명이 최대 길이(100자)를 초과하면 ValueError가 발생해야 한다.
        with self.assertRaisesRegex(ValueError, "배역명은 최대 100자까지 가능합니다."):
            ActorVO(name="배우이름", role_name="가" * 101)

    def test_create_with_external_id_too_long_raises_value_error(self):
        # 계약: 외부 ID가 최대 길이(100자)를 초과하면 ValueError가 발생해야 한다.
        with self.assertRaisesRegex(ValueError, "외부 ID는 최대 100자까지 가능합니다."):
            ActorVO(name="아이디테스트배우", external_id="a" * 101)

    def test_create_with_non_string_types_raises_type_error(self):
        # 계약: 이름, 배역명, 외부 ID가 문자열이 아닐 경우 TypeError가 발생해야 한다.
        with self.assertRaisesRegex(TypeError, "배역명은 문자열이어야 합니다."):
            ActorVO(name="타입테스트배우", role_name=123)
        with self.assertRaisesRegex(TypeError, "외부 ID는 문자열이어야 합니다."):
            ActorVO(name="타입테스트배우", external_id=True)

    def test_optional_fields_can_be_none(self):
        # 계약: 선택적 필드(role_name, external_id)는 None으로 설정될 수 있어야 한다.
        try:
            vo = ActorVO(name="필수이름만배우", role_name=None, external_id=None)
            self.assertIsNone(vo.role_name)
            self.assertIsNone(vo.external_id)
        except Exception as e:
            self.fail(f"선택적 필드에 None 할당 시 예외 발생: {e}")

    def test_actor_equality(self):
        # 계약: 두 ActorVO 객체는 모든 속성 값이 같으면 동등해야 한다.
        vo1 = ActorVO(name="동일배우", role_name="같은역할", external_id="ext1")
        vo2 = ActorVO(name="동일배우", role_name="같은역할", external_id="ext1")
        vo3 = ActorVO(name="다른배우", role_name="같은역할", external_id="ext1")
        vo4 = ActorVO(name="동일배우", role_name="다른역할", external_id="ext1")
        vo5 = ActorVO(name="동일배우")
        vo6 = ActorVO(name="동일배우")

        self.assertEqual(vo1, vo2)
        self.assertNotEqual(vo1, vo3)
        self.assertNotEqual(vo1, vo4)
        self.assertEqual(vo5, vo6)
        self.assertNotEqual(vo1, vo5)

    def test_actor_hash_consistency(self):
        # 계약: 동등한 ActorVO 객체는 동일한 해시 값을 가져야 한다.
        vo1 = ActorVO(name="해시값배우", role_name="역할1", external_id="hash_ext1")
        vo2 = ActorVO(name="해시값배우", role_name="역할1", external_id="hash_ext1")
        self.assertEqual(hash(vo1), hash(vo2))

    def test_actor_string_representation(self):
        # 계약: ActorVO 객체의 문자열 표현은 적절히 표시되어야 한다.
        vo_name_only = ActorVO(name="이병헌")
        self.assertEqual(str(vo_name_only), "이병헌")

        vo_with_role = ActorVO(name="마동석", role_name="마석도")
        self.assertEqual(str(vo_with_role), "마동석 (배역: 마석도)")


if __name__ == '__main__':
    unittest.main()