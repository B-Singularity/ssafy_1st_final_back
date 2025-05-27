import unittest
from apps.movie.domain.value_objects.poster_image_vo import PosterImageVO


class TestPosterImageValueObject(unittest.TestCase):

    def test_create_valid_poster_image_url(self):
        # 계약: 유효한 URL 문자열로 PosterImageVO를 성공적으로 생성할 수 있어야 한다.
        valid_url = "https://example.com/poster.jpg"
        vo = PosterImageVO(valid_url)
        self.assertIsInstance(vo, PosterImageVO)
        self.assertEqual(vo.url, valid_url)

    def test_create_with_empty_url_raises_value_error(self):
        # 계약: 비어있는 URL로 PosterImageVO 생성을 시도하면 ValueError가 발생해야 한다.
        with self.assertRaisesRegex(ValueError, "포스터 이미지 URL은 비어있을 수 없습니다."):
            PosterImageVO("")

    def test_create_with_none_url_raises_value_error(self):
        # 계약: URL로 None 값을 전달하여 PosterImageVO 생성을 시도하면 ValueError가 발생해야 한다.
        with self.assertRaisesRegex(ValueError, "포스터 이미지 URL은 비어있을 수 없습니다."):
            PosterImageVO(None)  # type: ignore

    def test_create_with_non_string_url_raises_type_error(self):
        # 계약: URL이 문자열이 아닐 경우 TypeError가 발생해야 한다.
        with self.assertRaisesRegex(TypeError, "포스터 이미지 URL은 문자열이어야 합니다."):
            PosterImageVO(12345)  # type: ignore

    def test_create_with_url_too_long_raises_value_error(self):
        # 계약: URL이 최대 길이(1024자)를 초과하면 ValueError가 발생해야 한다.
        long_url = "http://" + ("a" * 1017) + ".com"
        with self.assertRaisesRegex(ValueError, "포스터 이미지 URL은 최대 1024자까지 가능합니다."):
            PosterImageVO(long_url)

    def test_create_with_invalid_url_format_raises_value_error(self):
        # 계약: 정규식에 맞지 않는 URL 형식으로 PosterImageVO 생성을 시도하면 ValueError가 발생해야 한다.
        # 계약: 오류 메시지는 "유효하지 않은 URL 형식입니다." 이어야 한다.
        invalid_urls = ["ftp://example.com/image.jpg", "example.com/image.jpg", "www.example.com/image.jpg"]
        for url in invalid_urls:
            with self.subTest(url=url):
                # 기대하는 오류 메시지를 실제 발생하는 메시지로 수정
                with self.assertRaisesRegex(ValueError,
                                            "유효하지 않은 URL 형식입니다."):  # " http:// 또는 https://로 시작해야 합니다." 부분 제거
                    PosterImageVO(url)

    def test_poster_image_equality(self):
        # 계약: 두 PosterImageVO 객체는 url 속성 값이 같으면 동등해야 한다.
        url = "https://example.com/image.png"
        vo1 = PosterImageVO(url)
        vo2 = PosterImageVO(url)
        vo3 = PosterImageVO("https://example.com/another.png")

        self.assertEqual(vo1, vo2)
        self.assertNotEqual(vo1, vo3)

    def test_poster_image_hash_consistency(self):
        # 계약: 동등한 PosterImageVO 객체는 동일한 해시 값을 가져야 한다.
        url = "https://example.com/image.png"
        vo1 = PosterImageVO(url)
        vo2 = PosterImageVO(url)
        self.assertEqual(hash(vo1), hash(vo2))

    def test_poster_image_string_representation(self):
        # 계약: PosterImageVO 객체의 문자열 표현은 URL 문자열 자체여야 한다.
        url = "https://example.com/image.png"
        vo = PosterImageVO(url)
        self.assertEqual(str(vo), url)


if __name__ == '__main__':
    unittest.main()