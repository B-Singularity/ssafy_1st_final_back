import unittest
import re
from apps.movie.domain.value_objects.trailer_vo import TrailerVO


class TestTrailerValueObject(unittest.TestCase):

    def test_create_valid_trailer_all_fields(self):
        # 계약: 모든 필드가 유효한 값으로 TrailerVO를 성공적으로 생성할 수 있어야 한다.
        vo = TrailerVO(
            url="https://www.youtube.com/watch?v=trailer123",
            trailer_type="메인 예고편",
            site_name="YouTube",
            thumbnail_url="https://img.youtube.com/vi/trailer123/0.jpg"
        )
        self.assertEqual(vo.url, "https://www.youtube.com/watch?v=trailer123")
        self.assertEqual(vo.trailer_type, "메인 예고편")
        self.assertEqual(vo.site_name, "YouTube")
        self.assertEqual(vo.thumbnail_url, "https://img.youtube.com/vi/trailer123/0.jpg")

    def test_create_valid_trailer_url_only(self):
        # 계약: 필수 필드인 URL만으로 TrailerVO를 성공적으로 생성할 수 있어야 한다.
        vo = TrailerVO(url="http://example.com/trailer.mp4")
        self.assertEqual(vo.url, "http://example.com/trailer.mp4")
        self.assertIsNone(vo.trailer_type)
        self.assertIsNone(vo.site_name)
        self.assertIsNone(vo.thumbnail_url)

    def test_create_with_empty_url_raises_value_error(self):
        # 계약: 비어있는 URL로 생성 시도 시 ValueError가 발생해야 한다.
        with self.assertRaisesRegex(ValueError, "예고편 URL은 비어있을 수 없습니다."):
            TrailerVO(url="")

    def test_create_with_invalid_url_format_raises_value_error(self):
        # 계약: URL 형식이 유효하지 않으면 ValueError가 발생해야 한다.
        with self.assertRaisesRegex(ValueError, "유효하지 않은 예고편 URL 형식입니다: not_a_url"):
            TrailerVO(url="not_a_url")

    def test_create_with_invalid_thumbnail_url_format_raises_value_error(self):
        # 계약: 썸네일 URL 형식이 유효하지 않으면 ValueError가 발생해야 한다.
        with self.assertRaisesRegex(ValueError, "유효하지 않은 썸네일 URL 형식입니다: invalid_thumb_url"):
            TrailerVO(url="http://example.com/trailer.mp4", thumbnail_url="invalid_thumb_url")

    def test_create_with_trailer_type_too_long_raises_value_error(self):
        # 계약: 예고편 종류가 최대 길이(50자)를 초과하면 ValueError가 발생해야 한다.
        with self.assertRaisesRegex(ValueError, "예고편 종류는 최대 50자까지 가능합니다."):
            TrailerVO(url="http://a.com/trailer.mp4", trailer_type="가" * 51)

    def test_create_with_site_name_too_long_raises_value_error(self):
        # 계약: 사이트 이름이 최대 길이(50자)를 초과하면 ValueError가 발생해야 한다.
        with self.assertRaisesRegex(ValueError, "예고편 제공 사이트 이름은 최대 50자까지 가능합니다."):
            TrailerVO(url="http://a.com/trailer.mp4", site_name="가" * 51)

    def test_create_with_thumbnail_url_too_long_raises_value_error(self):
        # 계약: 썸네일 URL이 최대 길이(1024자)를 초과하면 ValueError가 발생해야 한다.
        with self.assertRaisesRegex(ValueError, "썸네일 URL은 최대 1024자까지 가능합니다."):
            TrailerVO(url="http://a.com/trailer.mp4", thumbnail_url="http://" + "a" * 1017 + ".com")

    def test_create_with_non_string_optional_fields_raises_type_error(self):
        # 계약: 선택적 문자열 필드가 문자열이 아니면(None 제외) TypeError가 발생해야 한다.
        with self.assertRaisesRegex(TypeError, "예고편 종류는 문자열이어야 합니다."):
            TrailerVO(url="http://a.com/trailer.mp4", trailer_type=123)
        with self.assertRaisesRegex(TypeError, "예고편 제공 사이트 이름은 문자열이어야 합니다."):
            TrailerVO(url="http://a.com/trailer.mp4", site_name=True)
        with self.assertRaisesRegex(TypeError, "썸네일 URL은 문자열이어야 합니다."):
            TrailerVO(url="http://a.com/trailer.mp4", thumbnail_url=456)

    def test_optional_fields_can_be_none(self):
        # 계약: 모든 선택적 필드는 None으로 설정될 수 있어야 한다.
        try:
            vo = TrailerVO(url="http://a.com/trailer.mp4", trailer_type=None, site_name=None, thumbnail_url=None)
            self.assertIsNone(vo.trailer_type)
            self.assertIsNone(vo.site_name)
            self.assertIsNone(vo.thumbnail_url)
        except Exception as e:
            self.fail(f"선택적 필드에 None 할당 시 예외 발생: {e}")

    def test_trailer_equality(self):
        # 계약: 두 TrailerVO 객체는 모든 속성 값이 같으면 동등해야 한다.
        url = "https://youtube.com/watch?v=1"
        ttype = "메인"
        sname = "YouTube"
        thumb = "https://youtube.com/thumb1.jpg"

        vo1 = TrailerVO(url, ttype, sname, thumb)
        vo2 = TrailerVO(url, ttype, sname, thumb)
        vo3 = TrailerVO(url, "티저", sname, thumb)  # trailer_type 다름

        self.assertEqual(vo1, vo2)
        self.assertNotEqual(vo1, vo3)

    def test_trailer_hash_consistency(self):
        # 계약: 동등한 TrailerVO 객체는 동일한 해시 값을 가져야 한다.
        url = "https://vimeo.com/12345"
        ttype = "단편"
        sname = "Vimeo"
        thumb = "https://vimeo.com/thumb_default.jpg"

        vo1 = TrailerVO(url, ttype, sname, thumb)
        vo2 = TrailerVO(url, ttype, sname, thumb)
        self.assertEqual(hash(vo1), hash(vo2))

    def test_trailer_string_representation(self):
        # 계약: TrailerVO 객체의 문자열 표현은 예고편 URL이어야 한다.
        url = "https://naver.tv/embed/123"
        vo = TrailerVO(url=url)
        self.assertEqual(str(vo), url)


if __name__ == '__main__':
    unittest.main()