import unittest
from apps.movie.domain.value_objects.genre_vo import GenreVO

class TestGenreValueObject(unittest.TestCase):

    def test_create_valid_genre(self):
        # 계약: 유효한 문자열로 GenreVO를 성공적으로 생성할 수 있어야 한다.
        genre_names = ["드라마", "액션", "코미디123"]
        for name in genre_names:
            with self.subTest(name=name):
                vo = GenreVO(name)
                self.assertIsInstance(vo, GenreVO)
                self.assertEqual(vo.name, name)

    def test_create_genre_with_stripping_whitespace(self):
        # 계약: 장르 이름 생성 시 앞뒤 공백은 제거되어야 한다.
        genre_name_with_space = "  액션  "
        expected_name = "액션"
        vo = GenreVO(genre_name_with_space)
        self.assertEqual(vo.name, expected_name)

    def test_create_with_empty_name_raises_value_error(self):
        # 계약: 비어있는 이름으로 GenreVO 생성을 시도하면 ValueError가 발생해야 한다.
        with self.assertRaisesRegex(ValueError, "장르 이름은 비어있을 수 없습니다."):
            GenreVO("")

    def test_create_with_none_name_raises_value_error(self):
        # 계약: 이름으로 None 값을 전달하여 GenreVO 생성을 시도하면 ValueError가 발생해야 한다.
        with self.assertRaisesRegex(ValueError, "장르 이름은 비어있을 수 없습니다."):
            GenreVO(None)  # type: ignore

    def test_create_with_non_string_name_raises_type_error(self):
        # 계약: 이름이 문자열이 아닐 경우 TypeError가 발생해야 한다.
        with self.assertRaisesRegex(TypeError, "장르 이름은 문자열이어야 합니다."):
            GenreVO(123)  # type: ignore

    def test_create_with_name_too_long_raises_value_error(self):
        # 계약: 이름이 최대 길이(50자)를 초과하면 ValueError가 발생해야 한다.
        long_name = "가" * 51
        with self.assertRaisesRegex(ValueError, "장르 이름은 최대 50자까지 가능합니다."):
            GenreVO(long_name)

    # VALID_GENRES 목록 검증 관련 테스트는 현재 제외됨
    # def test_create_with_invalid_genre_from_list_raises_value_error(self):
    #     # 계약: (만약 활성화되었다면) VALID_GENRES 목록에 없는 장르로 생성 시도 시 ValueError가 발생해야 한다.
    #     pass

    def test_genre_equality(self):
        # 계약: 두 GenreVO 객체는 name 속성 값이 같으면 동등해야 한다.
        vo1 = GenreVO("드라마")
        vo2 = GenreVO("드라마")
        vo3 = GenreVO("액션")

        self.assertEqual(vo1, vo2)
        self.assertNotEqual(vo1, vo3)

    def test_genre_hash_consistency(self):
        # 계약: 동등한 GenreVO 객체는 동일한 해시 값을 가져야 한다.
        vo1 = GenreVO("스릴러")
        vo2 = GenreVO("스릴러")
        self.assertEqual(hash(vo1), hash(vo2))

    def test_genre_string_representation(self):
        # 계약: GenreVO 객체의 문자열 표현은 장르 이름 자체여야 한다.
        genre_name = "코미디"
        vo = GenreVO(genre_name)
        self.assertEqual(str(vo), genre_name)


if __name__ == '__main__':
    unittest.main()