import unittest
from apps.movie.domain.value_objects.movie_platform_rating_vo import MoviePlatformRatingVO

class TestMoviePlatformRatingValueObject(unittest.TestCase):

    def test_create_valid_rating(self):
        # 계약: 유효한 플랫폼 이름과 점수로 MoviePlatformRatingVO를 성공적으로 생성할 수 있어야 한다.
        vo = MoviePlatformRatingVO(platform_name="IMDB", score=8.7)
        self.assertEqual(vo.platform_name, "IMDB")
        self.assertEqual(vo.score, 8.7)

    def test_create_with_empty_platform_name_raises_value_error(self):
        # 계약: 비어있는 플랫폼 이름으로 생성 시도 시 ValueError가 발생해야 한다.
        with self.assertRaisesRegex(ValueError, "평가 플랫폼 이름은 비어있을 수 없습니다."):
            MoviePlatformRatingVO(platform_name="", score=7.0)

    def test_create_with_platform_name_too_long_raises_value_error(self):
        # 계약: 플랫폼 이름이 최대 길이(100자)를 초과하면 ValueError가 발생해야 한다.
        long_name = "플" * 101
        with self.assertRaisesRegex(ValueError, "평가 플랫폼 이름은 유효한 문자열이어야 하며 최대 100자입니다."):
            MoviePlatformRatingVO(platform_name=long_name, score=7.0)


    def test_create_with_score_out_of_range_raises_value_error(self):
        # 계약: 평점이 유효 범위(0.0~10.0)를 벗어나면 ValueError가 발생해야 한다.
        with self.assertRaisesRegex(ValueError, "평점은 0.0에서 10.0 사이의 값이어야 합니다."):
            MoviePlatformRatingVO(platform_name="TestFlix", score=11.0)
        with self.assertRaisesRegex(ValueError, "평점은 0.0에서 10.0 사이의 값이어야 합니다."):
            MoviePlatformRatingVO(platform_name="TestFlix", score=-0.5)

    def test_create_with_non_numeric_score_raises_type_error(self):
        # 계약: 평점이 숫자가 아닐 경우 TypeError가 발생해야 한다.
        with self.assertRaisesRegex(TypeError, "평점은 숫자\\(정수 또는 실수\\)여야 합니다."):
            MoviePlatformRatingVO(platform_name="TestFlix", score="높음")

    def test_rating_equality(self):
        # 계약: 두 MoviePlatformRatingVO 객체는 플랫폼 이름과 점수가 모두 같으면 동등해야 한다.
        vo1 = MoviePlatformRatingVO("IMDB", 8.5)
        vo2 = MoviePlatformRatingVO("IMDB", 8.5)
        vo3 = MoviePlatformRatingVO("왓챠", 8.5)
        vo4 = MoviePlatformRatingVO("IMDB", 8.6)

        self.assertEqual(vo1, vo2)
        self.assertNotEqual(vo1, vo3)
        self.assertNotEqual(vo1, vo4)

    def test_rating_hash_consistency(self):
        # 계약: 동등한 MoviePlatformRatingVO 객체는 동일한 해시 값을 가져야 한다.
        vo1 = MoviePlatformRatingVO("네이버 영화", 9.0)
        vo2 = MoviePlatformRatingVO("네이버 영화", 9.0)
        self.assertEqual(hash(vo1), hash(vo2))

    def test_rating_string_representation(self):
        # 계약: MoviePlatformRatingVO 객체의 문자열 표현은 "플랫폼명: 점수/10" 형식이어야 한다.
        vo = MoviePlatformRatingVO("TMDB", 8.0)
        self.assertEqual(str(vo), "TMDB: 8.0/10")

if __name__ == '__main__':
    unittest.main()