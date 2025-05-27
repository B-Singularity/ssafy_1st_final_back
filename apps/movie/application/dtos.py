from typing import List, Optional, Dict
from datetime import date, datetime


class FilterOptionsDto:
    def __init__(self,
                 genres: Optional[List[str]] = None,
                 release_year_from: Optional[int] = None,
                 release_year_to: Optional[int] = None):
        if genres is not None and not isinstance(genres, list):
            raise TypeError("장르 필터는 문자열 리스트여야 합니다.")
        self.genres = genres
        self.release_year_from = release_year_from
        self.release_year_to = release_year_to
        # production_countries 속성 제거


class SortOptionDto:
    def __init__(self, field, direction, rating_platform=None):
        print(
            f"--- [DTO Init] SortOptionDto: field='{field}', direction='{direction}', rating_platform='{rating_platform}', type(rating_platform)='{type(rating_platform)}' ---")  # ⭐️ 디버그 프린트

        if not field:
            raise ValueError("정렬 기준 필드는 비어있을 수 없습니다.")

        direction_lower = str(direction).lower()
        if direction_lower not in ['asc', 'desc']:
            raise ValueError("정렬 방향은 'asc' 또는 'desc'여야 합니다.")

        # rating_platform이 None이거나, 공백만 있는 문자열인지 더 명확하게 확인
        is_rating_platform_provided = rating_platform is not None and isinstance(rating_platform,
                                                                                 str) and rating_platform.strip() != ""

        if field == "rating" and not is_rating_platform_provided:
            print(
                f"--- [DTO Error] SortOptionDto: field is 'rating' but rating_platform is not provided or empty. Value: '{rating_platform}' ---")  # ⭐️ 디버그 프린트
            raise ValueError("평점 정렬 시 'rating_platform'을 지정해야 합니다.")

        if rating_platform is not None and not isinstance(rating_platform, str):
            # 이 검사는 is_rating_platform_provided에서 이미 어느 정도 커버됨
            raise TypeError("rating_platform은 문자열이어야 합니다.")

        self.field = field
        self.direction = direction_lower
        self.rating_platform = rating_platform.strip() if isinstance(rating_platform, str) and rating_platform else None


class PaginationDto:
    def __init__(self, page_number: int = 1, page_size: int = 20):
        if not isinstance(page_number, int) or page_number < 1:
            raise ValueError("페이지 번호는 1 이상의 정수여야 합니다.")
        if not isinstance(page_size, int) or not (1 <= page_size <= 100):
            raise ValueError("페이지 크기는 1에서 100 사이의 정수여야 합니다.")
        self.page_number = page_number
        self.page_size = page_size


class MovieSearchCriteriaDto:
    def __init__(self,
                 keyword: Optional[str] = None,
                 filters: Optional[FilterOptionsDto] = None,
                 sort_by: Optional[SortOptionDto] = None,
                 pagination: Optional[PaginationDto] = None):
        if keyword is not None and (not isinstance(keyword, str) or len(keyword) > 100):
            raise ValueError("검색어는 최대 100자의 문자열이어야 합니다.")
        self.keyword = keyword
        self.filters = filters if filters else FilterOptionsDto()
        self.sort_by = sort_by
        self.pagination = pagination if pagination else PaginationDto()


class SearchedMovieItemDto:
    def __init__(self, movie_id: int, title: str, poster_image_url: Optional[str], release_year: Optional[int],
                 rating: Optional[float]):
        self.movie_id = movie_id
        self.title = title
        self.poster_image_url = poster_image_url
        self.release_year = release_year
        self.rating = rating


class MovieSearchResultDto:
    def __init__(self,
                 movies: List[SearchedMovieItemDto],
                 total_results: int,
                 current_page: int,
                 total_pages: int,
                 message: Optional[str] = None):
        self.movies = movies
        self.total_results = total_results
        self.current_page = current_page
        self.total_pages = total_pages
        self.message = message


class TitleInfoDisplayDto:
    def __init__(self, korean_title: str, original_title: Optional[str]):
        self.korean_title = korean_title
        self.original_title = original_title


class PlotDisplayDto:
    def __init__(self, text: Optional[str]):
        self.text = text


class StillCutDisplayDto:
    def __init__(self, image_url: str, caption: Optional[str], display_order: int):
        self.image_url = image_url
        self.caption = caption
        self.display_order = display_order


class TrailerDisplayDto:
    def __init__(self, url: str, trailer_type: Optional[str], site_name: Optional[str], thumbnail_url: Optional[str]):
        self.url = url
        self.trailer_type = trailer_type
        self.site_name = site_name
        self.thumbnail_url = thumbnail_url


class MoviePlatformRatingDisplayDto:
    def __init__(self, platform_name: str, score: float):
        self.platform_name = platform_name
        self.score = score


class OTTInfoDisplayDto:
    def __init__(self, platform_name: str, watch_url: Optional[str], logo_image_url: Optional[str],
                 availability_note: Optional[str]):
        self.platform_name = platform_name
        self.watch_url = watch_url
        self.logo_image_url = logo_image_url
        self.availability_note = availability_note


class MovieDetailDto:
    def __init__(self,
                 movie_id: int,
                 title_info: TitleInfoDisplayDto,
                 plot: PlotDisplayDto,
                 release_date_str: str,
                 runtime_minutes: int,
                 poster_image_url: str,
                 genres: List[str],
                 directors: List[str],
                 cast: List[str],
                 still_cuts: List[StillCutDisplayDto],
                 trailers: List[TrailerDisplayDto],
                 platform_ratings: List[MoviePlatformRatingDisplayDto],
                 ott_availability: List[OTTInfoDisplayDto],
                 created_at_str: str,
                 updated_at_str: Optional[str]):
        self.movie_id = movie_id
        self.title_info = title_info
        self.plot = plot
        self.release_date_str = release_date_str
        self.runtime_minutes = runtime_minutes
        self.poster_image_url = poster_image_url
        self.genres = genres
        self.directors = directors
        self.cast = cast
        self.still_cuts = still_cuts
        self.trailers = trailers
        self.platform_ratings = platform_ratings
        self.ott_availability = ott_availability
        self.created_at_str = created_at_str
        self.updated_at_str = updated_at_str