import unittest
import re
from apps.movie.domain.value_objects.ott_info_vo import OTTInfoVO


class TestOTTInfoValueObject(unittest.TestCase):

    def test_create_valid_ott_info_all_fields(self):
        vo = OTTInfoVO(
            platform_name="Netflix",
            watch_url="https://www.netflix.com/title/12345",
            logo_image_url="https://example.com/netflix_logo.png",
            availability_note="4K 구독 필요"
        )
        self.assertEqual(vo.platform_name, "Netflix")
        self.assertEqual(vo.watch_url, "https://www.netflix.com/title/12345")
        self.assertEqual(vo.logo_image_url, "https://example.com/netflix_logo.png")
        self.assertEqual(vo.availability_note, "4K 구독 필요")

    def test_create_valid_ott_info_platform_name_only(self):
        vo = OTTInfoVO(platform_name="왓챠")
        self.assertEqual(vo.platform_name, "왓챠")
        self.assertIsNone(vo.watch_url)
        self.assertIsNone(vo.logo_image_url)
        self.assertIsNone(vo.availability_note)

    def test_create_with_empty_platform_name_raises_value_error(self):
        with self.assertRaisesRegex(ValueError, "OTT 플랫폼 이름은 비어있을 수 없습니다."):
            OTTInfoVO(platform_name="")

    def test_create_with_invalid_watch_url_raises_value_error(self):
        with self.assertRaisesRegex(ValueError, "유효하지 않은 시청 URL 형식입니다: invalid_url"):
            OTTInfoVO(platform_name="TestOTT", watch_url="invalid_url")

    def test_create_with_invalid_logo_url_raises_value_error(self):
        with self.assertRaisesRegex(ValueError, "유효하지 않은 플랫폼 로고 URL 형식입니다: bad_logo_url"):
            OTTInfoVO(platform_name="TestOTT", logo_image_url="bad_logo_url")

    def test_create_with_note_too_long_raises_value_error(self):
        with self.assertRaisesRegex(ValueError, "이용 정보 안내는 최대 100자까지 가능합니다."):
            OTTInfoVO(platform_name="TestOTT", availability_note="가" * 101)

    def test_create_with_non_string_optional_fields_raises_type_error(self):
        with self.assertRaisesRegex(TypeError, "시청 URL은 문자열이어야 합니다."):
            OTTInfoVO(platform_name="TestOTT", watch_url=123)
        with self.assertRaisesRegex(TypeError, "플랫폼 로고 URL은 문자열이어야 합니다."):
            OTTInfoVO(platform_name="TestOTT", logo_image_url=True)
        with self.assertRaisesRegex(TypeError, "이용 정보 안내는 문자열이어야 합니다."):
            OTTInfoVO(platform_name="TestOTT", availability_note=456)

    def test_ott_info_equality(self):
        # 계약: 두 OTTInfoVO 객체는 모든 속성 값이 같으면 동등해야 한다.
        # URL 필드에 유효한 URL 또는 None을 사용하도록 수정
        vo1 = OTTInfoVO("Netflix", "https://url1.com", "https://logo1.com", "note1")
        vo2 = OTTInfoVO("Netflix", "https://url1.com", "https://logo1.com", "note1")
        vo3 = OTTInfoVO("왓챠", "https://url1.com", "https://logo1.com", "note1")
        vo4 = OTTInfoVO("Netflix", None, None, "note1")  # URL 필드는 None일 수 있음
        vo5 = OTTInfoVO("Netflix", None, None, "note1")

        self.assertEqual(vo1, vo2)
        self.assertNotEqual(vo1, vo3)
        self.assertEqual(vo4, vo5)
        self.assertNotEqual(vo1, vo4)

    def test_ott_info_hash_consistency(self):
        # 계약: 동등한 OTTInfoVO 객체는 동일한 해시 값을 가져야 한다.
        # URL 필드에 유효한 URL 또는 None을 사용하도록 수정
        vo1 = OTTInfoVO("티빙", "https://url_tving.com", "https://logo_tving.com", "티빙 오리지널")
        vo2 = OTTInfoVO("티빙", "https://url_tving.com", "https://logo_tving.com", "티빙 오리지널")
        vo_none_urls = OTTInfoVO("티빙", None, None, "티빙 오리지널")
        vo_none_urls2 = OTTInfoVO("티빙", None, None, "티빙 오리지널")

        self.assertEqual(hash(vo1), hash(vo2))
        self.assertEqual(hash(vo_none_urls), hash(vo_none_urls2))
        self.assertNotEqual(hash(vo1), hash(vo_none_urls))

    def test_ott_info_string_representation(self):
        vo_with_note = OTTInfoVO(platform_name="디즈니+", availability_note="월트 디즈니 컴퍼니")
        self.assertEqual(str(vo_with_note), "디즈니+ (월트 디즈니 컴퍼니)")

        vo_name_only = OTTInfoVO(platform_name="Apple TV+")
        self.assertEqual(str(vo_name_only), "Apple TV+")


if __name__ == '__main__':
    unittest.main()