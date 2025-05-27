import unittest
import re
from apps.movie.domain.value_objects.still_cut_vo import StillCutVO


class TestStillCutValueObject(unittest.TestCase):

    def test_create_valid_still_cut_all_fields(self):
        # 계약: 모든 필드가 유효한 값으로 StillCutVO를 성공적으로 생성할 수 있어야 한다.
        vo = StillCutVO(image_url="https://example.com/still.jpg", caption="명장면", display_order=1)
        self.assertEqual(vo.image_url, "https://example.com/still.jpg")
        self.assertEqual(vo.caption, "명장면")
        self.assertEqual(vo.display_order, 1)

    def test_create_valid_still_cut_url_only(self):
        # 계약: 필수 필드인 이미지 URL만으로 StillCutVO를 성공적으로 생성할 수 있어야 한다.
        vo = StillCutVO(image_url="http://localhost:8000/another.png")  # localhost도 허용
        self.assertEqual(vo.image_url, "http://localhost:8000/another.png")
        self.assertIsNone(vo.caption)
        self.assertEqual(vo.display_order, 0)

    def test_create_with_empty_image_url_raises_value_error(self):
        # 계약: 비어있는 이미지 URL로 생성 시도 시 ValueError가 발생해야 한다.
        with self.assertRaisesRegex(ValueError, "스틸컷 이미지 URL은 비어있을 수 없습니다."):
            StillCutVO(image_url="")

    def test_create_with_invalid_url_format_raises_value_error(self):
        # 계약: 정규식에 맞지 않는 URL 형식으로 StillCutVO 생성을 시도하면 ValueError가 발생해야 한다.
        invalid_urls = [
            "ftp://example.com/image.jpg",  # ftp 스킴은 이제 제외됨
            "example.com/image.jpg",  # 스킴 없음
            "www.example.com/image.jpg",  # 스킴 없음
            "http//example.com/image.jpg",  # 슬래시 누락
            "https://example",  # TLD 없음 (단, 정규식에 따라 다를 수 있음. 현재 정규식은 허용할 수도)
            "https://.com"  # 도메인 없음
        ]
        for url in invalid_urls:
            with self.subTest(url=url):
                with self.assertRaisesRegex(ValueError, "유효하지 않은 스틸컷 이미지 URL 형식입니다."):
                    StillCutVO(image_url=url)

    def test_create_valid_ip_url(self):
        # 계약: 유효한 IP 주소 기반 URL로도 생성이 가능해야 한다.
        valid_ip_url = "http://127.0.0.1/image.png"
        try:
            vo = StillCutVO(valid_ip_url)
            self.assertEqual(vo.image_url, valid_ip_url)
        except ValueError:
            self.fail("IP 주소 기반 URL 생성에 실패했습니다.")

    def test_create_with_caption_too_long_raises_value_error(self):
        # 계약: 캡션이 최대 길이(255자)를 초과하면 ValueError가 발생해야 한다.
        with self.assertRaisesRegex(ValueError, "스틸컷 캡션은 최대 255자까지 가능합니다."):
            StillCutVO(image_url="http://a.com/b.jpg", caption="가" * 256)

    def test_create_with_negative_display_order_raises_value_error(self):
        # 계약: 표시 순서가 음수이면 ValueError가 발생해야 한다.
        with self.assertRaisesRegex(ValueError, "스틸컷 표시 순서는 0 이상의 정수여야 합니다."):
            StillCutVO(image_url="http://a.com/c.jpg", display_order=-1)

    def test_create_with_non_string_caption_raises_type_error(self):
        # 계약: 캡션이 문자열이 아니면(None 제외) TypeError가 발생해야 한다.
        with self.assertRaisesRegex(TypeError, "스틸컷 캡션은 문자열이어야 합니다."):
            StillCutVO(image_url="http://a.com/d.jpg", caption=123)

    def test_create_with_non_integer_display_order_raises_value_error(self):
        # 계약: 표시 순서가 정수가 아니면 ValueError가 발생해야 한다.
        with self.assertRaisesRegex(ValueError, "스틸컷 표시 순서는 0 이상의 정수여야 합니다."):
            StillCutVO(image_url="http://a.com/e.jpg", display_order="first")

    def test_optional_caption_can_be_none(self):
        # 계약: 선택적 필드인 caption은 None으로 설정될 수 있어야 한다.
        try:
            vo = StillCutVO(image_url="http://a.com/f.jpg", caption=None, display_order=0)
            self.assertIsNone(vo.caption)
        except Exception as e:
            self.fail(f"caption에 None 할당 시 예외 발생: {e}")

    def test_still_cut_equality(self):
        # 계약: 두 StillCutVO 객체는 모든 속성 값이 같으면 동등해야 한다.
        vo1 = StillCutVO(image_url="https://url1.com", caption="캡션1", display_order=1)
        vo2 = StillCutVO(image_url="https://url1.com", caption="캡션1", display_order=1)
        vo3 = StillCutVO(image_url="https://url2.com", caption="캡션1", display_order=1)
        self.assertEqual(vo1, vo2)
        self.assertNotEqual(vo1, vo3)

    def test_still_cut_hash_consistency(self):
        # 계약: 동등한 StillCutVO 객체는 동일한 해시 값을 가져야 한다.
        vo1 = StillCutVO(image_url="https://url_hash.com", caption="해시캡션", display_order=2)
        vo2 = StillCutVO(image_url="https://url_hash.com", caption="해시캡션", display_order=2)
        self.assertEqual(hash(vo1), hash(vo2))

    def test_still_cut_string_representation(self):
        # 계약: StillCutVO 객체의 문자열 표현은 이미지 URL이어야 한다.
        url = "https://example.com/my_still.jpg"
        vo = StillCutVO(image_url=url)
        self.assertEqual(str(vo), url)


if __name__ == '__main__':
    unittest.main()