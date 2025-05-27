import unittest
from apps.movie.domain.value_objects.director_vo import DirectorVO

class TestDirectorValueObject(unittest.TestCase):

    def test_create_valid_director_all_fields(self):
        # 계약: 이름과 외부 ID가 유효한 값으로 DirectorVO를 성공적으로 생성할 수 있어야 한다.
        vo = DirectorVO(name="봉준호", external_id="imdb_dir_123")
        self.assertEqual(vo.name, "봉준호")
        self.assertEqual(vo.external_id, "imdb_dir_123")

    def test_create_valid_director_name_only(self):
        # 계약: 필수 필드인 이름만으로 DirectorVO를 성공적으로 생성할 수 있어야 한다.
        vo = DirectorVO(name="박찬욱")
        self.assertEqual(vo.name, "박찬욱")
        self.assertIsNone(vo.external_id)

    def test_create_with_empty_name_raises_value_error(self):
        # 계약: 비어있는 이름으로 생성 시도 시 ValueError가 발생해야 한다.
        with self.assertRaisesRegex(ValueError, "감독 이름은 비어있을 수 없습니다."):
            DirectorVO(name="")

    def test_create_with_name_too_long_raises_value_error(self):
        # 계약: 이름이 최대 길이(100자)를 초과하면 ValueError가 발생해야 한다.
        with self.assertRaisesRegex(ValueError, "감독 이름은 유효한 문자열이어야 하며 최대 100자입니다."):
            DirectorVO(name="김" * 101)

    def test_create_with_external_id_too_long_raises_value_error(self):
        # 계약: 외부 ID가 최대 길이(100자)를 초과하면 ValueError가 발생해야 한다.
        with self.assertRaisesRegex(ValueError, "외부 ID는 최대 100자까지 가능합니다."):
            DirectorVO(name="아이디테스트감독", external_id="a" * 101)

    def test_create_with_non_string_external_id_raises_type_error(self):
        # 계약: 외부 ID가 문자열이 아닐 경우 TypeError가 발생해야 한다.
        with self.assertRaisesRegex(TypeError, "외부 ID는 문자열이어야 합니다."):
            DirectorVO(name="타입테스트감독", external_id=True)

    def test_optional_fields_can_be_none(self):
        # 계약: 선택적 필드(external_id)는 None으로 설정될 수 있어야 한다.
        try:
            vo = DirectorVO(name="필수이름만감독", external_id=None)
            self.assertIsNone(vo.external_id)
        except Exception as e:
            self.fail(f"선택적 필드에 None 할당 시 예외 발생: {e}")

    def test_director_equality(self):
        # 계약: 두 DirectorVO 객체는 모든 속성 값이 같으면 동등해야 한다.
        vo1 = DirectorVO(name="동일감독", external_id="ext1")
        vo2 = DirectorVO(name="동일감독", external_id="ext1")
        vo3 = DirectorVO(name="다른감독", external_id="ext1")
        vo4 = DirectorVO(name="동일감독")
        vo5 = DirectorVO(name="동일감독")

        self.assertEqual(vo1, vo2)
        self.assertNotEqual(vo1, vo3)
        self.assertEqual(vo4, vo5)

    def test_director_hash_consistency(self):
        # 계약: 동등한 DirectorVO 객체는 동일한 해시 값을 가져야 한다.
        vo1 = DirectorVO(name="해시값감독", external_id="hash_ext1")
        vo2 = DirectorVO(name="해시값감독", external_id="hash_ext1")
        self.assertEqual(hash(vo1), hash(vo2))

    def test_director_string_representation(self):
        # 계약: DirectorVO 객체의 문자열 표현은 감독 이름이어야 한다.
        vo = DirectorVO(name="크리스토퍼 놀란")
        self.assertEqual(str(vo), "크리스토퍼 놀란")

if __name__ == '__main__':
    unittest.main()