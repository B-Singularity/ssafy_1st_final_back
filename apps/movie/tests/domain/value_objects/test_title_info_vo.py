import unittest
from apps.movie.domain.value_objects.title_info_vo import TitleInfoVO


class TestTitleInfoValueObject(unittest.TestCase):

    def test_create_valid_title_info(self):
        # 계약: 유효한 한국어 제목과 (선택적) 원제로 TitleInfoVO를 성공적으로 생성할 수 있어야 한다.
        title_vo1 = TitleInfoVO(korean_title="범죄도시4")
        self.assertEqual(title_vo1.korean_title, "범죄도시4")
        self.assertIsNone(title_vo1.original_title)

        title_vo2 = TitleInfoVO(korean_title="웡카", original_title="Wonka")
        self.assertEqual(title_vo2.korean_title, "웡카")
        self.assertEqual(title_vo2.original_title, "Wonka")

    def test_create_with_empty_korean_title_raises_value_error(self):
        # 계약: 비어있는 한국어 제목으로 TitleInfoVO 생성을 시도하면 ValueError가 발생해야 한다.
        # 계약: 오류 메시지는 "한국어 영화 제목은 비어있을 수 없습니다." 이어야 한다.
        with self.assertRaisesRegex(ValueError, "한국어 영화 제목은 비어있을 수 없습니다."):
            TitleInfoVO(korean_title="")

    def test_create_with_korean_title_too_long_raises_value_error(self):
        # 계약: 한국어 제목이 최대 길이(255자)를 초과하면 ValueError가 발생해야 한다.
        long_title = "가" * 256
        with self.assertRaisesRegex(ValueError, "한국어 영화 제목은 최대 255자까지 가능합니다."):
            TitleInfoVO(korean_title=long_title)

    def test_create_with_original_title_too_long_raises_value_error(self):
        # 계약: 원제가 최대 길이(255자)를 초과하면 ValueError가 발생해야 한다.
        long_title = "O" * 256
        with self.assertRaisesRegex(ValueError, "원제는 최대 255자까지 가능합니다."):
            TitleInfoVO(korean_title="정상 제목", original_title=long_title)

    def test_create_with_non_string_original_title_raises_type_error(self):
        # 계약: 원제가 문자열이 아닌 타입(None 제외)으로 전달되면 TypeError가 발생해야 한다.
        with self.assertRaisesRegex(TypeError, "원제는 문자열이어야 합니다."):
            TitleInfoVO(korean_title="정상 제목", original_title=123)  # type: ignore

    def test_title_info_equality(self):
        # 계약: 두 TitleInfoVO 객체는 korean_title과 original_title이 모두 같으면 동등해야 한다.
        title1 = TitleInfoVO(korean_title="웡카", original_title="Wonka")
        title2 = TitleInfoVO(korean_title="웡카", original_title="Wonka")
        title3 = TitleInfoVO(korean_title="웡카", original_title="Wonka khác")
        title4 = TitleInfoVO(korean_title="다른 제목", original_title="Wonka")
        title5 = TitleInfoVO(korean_title="웡카")
        title6 = TitleInfoVO(korean_title="웡카")

        self.assertEqual(title1, title2)
        self.assertNotEqual(title1, title3)
        self.assertNotEqual(title1, title4)
        self.assertNotEqual(title1, title5)  # original_title이 None인 경우
        self.assertEqual(title5, title6)

    def test_title_info_hash_consistency(self):
        # 계약: 동등한 TitleInfoVO 객체는 동일한 해시 값을 가져야 한다.
        title1 = TitleInfoVO(korean_title="웡카", original_title="Wonka")
        title2 = TitleInfoVO(korean_title="웡카", original_title="Wonka")
        title5 = TitleInfoVO(korean_title="웡카")
        title6 = TitleInfoVO(korean_title="웡카")

        self.assertEqual(hash(title1), hash(title2))
        self.assertEqual(hash(title5), hash(title6))
        self.assertNotEqual(hash(title1), hash(title5))

    def test_title_info_string_representation(self):
        # 계약: TitleInfoVO 객체의 문자열 표현은 적절히 표시되어야 한다.
        title_ko_only = TitleInfoVO(korean_title="범죄도시4")
        self.assertEqual(str(title_ko_only), "범죄도시4")

        title_with_original = TitleInfoVO(korean_title="웡카", original_title="Wonka")
        self.assertEqual(str(title_with_original), "웡카 (Wonka)")

        title_same_ko_original = TitleInfoVO(korean_title="매트릭스", original_title="매트릭스")
        self.assertEqual(str(title_same_ko_original), "매트릭스")


if __name__ == '__main__':
    unittest.main()