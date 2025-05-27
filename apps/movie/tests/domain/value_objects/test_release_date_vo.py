import unittest
from datetime import date, timedelta
from apps.movie.domain.value_objects.release_date_vo import ReleaseDateVO


class TestReleaseDateValueObject(unittest.TestCase):

    def test_create_valid_release_date(self):
        # 계약: 유효한 date 객체로 ReleaseDateVO를 성공적으로 생성할 수 있어야 한다.
        today = date.today()
        release_date_vo = ReleaseDateVO(today)
        self.assertIsInstance(release_date_vo, ReleaseDateVO)
        self.assertEqual(release_date_vo.release_date, today)

    def test_create_with_non_date_type_raises_type_error(self):
        # 계약: date 객체가 아닌 타입으로 ReleaseDateVO 생성을 시도하면 TypeError가 발생해야 한다.
        # 계약: 오류 메시지는 "개봉일은 유효한 date 객체여야 합니다." 이어야 한다.
        invalid_inputs = ["2023-01-01", None, 123]
        for invalid_input in invalid_inputs:
            with self.subTest(invalid_input=invalid_input):
                with self.assertRaisesRegex(TypeError, "개봉일은 유효한 date 객체여야 합니다."):
                    ReleaseDateVO(invalid_input)  # type: ignore

    def test_formatted_method_default(self):
        # 계약: formatted 메서드는 기본 형식("%Y년 %m월 %d일")으로 날짜 문자열을 반환해야 한다.
        test_date = date(2023, 10, 26)
        release_date_vo = ReleaseDateVO(test_date)
        self.assertEqual(release_date_vo.formatted(), "2023년 10월 26일")

    def test_formatted_method_custom_format(self):
        # 계약: formatted 메서드는 사용자 정의 형식으로 날짜 문자열을 반환해야 한다.
        test_date = date(2023, 5, 1)
        release_date_vo = ReleaseDateVO(test_date)
        self.assertEqual(release_date_vo.formatted("%Y-%m-%d"), "2023-05-01")

    def test_release_date_equality(self):
        # 계약: 두 ReleaseDateVO 객체는 내부 date 객체가 같으면 동등해야 한다.
        date1 = date(2024, 1, 1)
        date2 = date(2024, 1, 1)
        date3 = date(2024, 1, 2)

        vo1 = ReleaseDateVO(date1)
        vo2 = ReleaseDateVO(date2)
        vo3 = ReleaseDateVO(date3)

        self.assertEqual(vo1, vo2)
        self.assertNotEqual(vo1, vo3)

    def test_release_date_hash_consistency(self):
        # 계약: 동등한 ReleaseDateVO 객체는 동일한 해시 값을 가져야 한다.
        date1 = date(2024, 1, 1)
        date2 = date(2024, 1, 1)

        vo1 = ReleaseDateVO(date1)
        vo2 = ReleaseDateVO(date2)
        self.assertEqual(hash(vo1), hash(vo2))

    def test_release_date_string_representation(self):
        # 계약: ReleaseDateVO 객체의 문자열 표현은 기본 포맷된 날짜 문자열이어야 한다.
        test_date = date(2023, 7, 7)
        release_date_vo = ReleaseDateVO(test_date)
        self.assertEqual(str(release_date_vo), "2023년 07월 07일")


if __name__ == '__main__':
    unittest.main()