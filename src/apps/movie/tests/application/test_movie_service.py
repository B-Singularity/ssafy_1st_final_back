import pytest
from unittest.mock import MagicMock
from datetime import datetime

from src.apps.movie.application.services import MovieAppService
from src.apps.movie.application.dtos import MovieDetailDto, PaginationDto, MovieSearchCriteriaDto, MovieSearchResultDto


@pytest.fixture
def mock_repositories():
    mock_movie_repo = MagicMock()
    mock_search_repo = MagicMock()
    return mock_movie_repo, mock_search_repo

# 계약: get_movie_details 호출 시, 리포지토리가 영화 데이터를 성공적으로 찾으면,
#       서비스는 해당 데이터를 MovieDetailDto로 올바르게 변환하여 반환해야 한다.

def test_get_movie_details_success(mock_repositories):
    # --- 1. 준비 (Arrange) ---
    mock_movie_repo, mock_search_repo = mock_repositories

    # 리포지토리가 반환할 가상의 Movie 애그리거트 Mock 객체를 상세하게 설정합니다.
    mock_movie_aggregate = MagicMock()
    mock_movie_aggregate.movie_id = 123
    mock_movie_aggregate.title_info.korean_title = "테스트 영화"
    mock_movie_aggregate.title_info.original_title = "Test Movie"
    mock_movie_aggregate.plot.text = "영화 줄거리입니다."
    mock_movie_aggregate.release_date.formatted.return_value = "2025년 06월 20일"
    mock_movie_aggregate.runtime.minutes = 120
    mock_movie_aggregate.poster_image.url = "http://example.com/poster.jpg"

    # --- 여기부터 수정된 부분 ---
    mock_genre_drama = MagicMock()
    mock_genre_drama.name = "드라마"
    mock_genre_action = MagicMock()
    mock_genre_action.name = "액션"
    mock_movie_aggregate.genres = [mock_genre_drama, mock_genre_action]
    # --- 여기까지 수정된 부분 ---

    mock_director = MagicMock()
    mock_director.name = "김감독"
    mock_movie_aggregate.directors = [mock_director]

    mock_cast = MagicMock()
    mock_cast.name = "이배우"
    mock_cast.role_name = "주인공"
    mock_movie_aggregate.cast = [mock_cast]

    mock_movie_aggregate.still_cuts = []
    mock_movie_aggregate.trailers = []
    mock_movie_aggregate.platform_ratings = []
    mock_movie_aggregate.ott_availability = []
    mock_movie_aggregate.created_at = datetime(2025, 6, 20, 12, 0, 0)
    mock_movie_aggregate.updated_at = datetime(2025, 6, 20, 12, 0, 0)

    mock_movie_repo.find_by_id.return_value = mock_movie_aggregate

    service = MovieAppService(mock_movie_repo, mock_search_repo)

    # --- 2. 실행 (Act) ---
    result_dto = service.get_movie_details(movie_id=123)

    # --- 3. 검증 (Assert) ---
    mock_movie_repo.find_by_id.assert_called_once_with(123)
    assert isinstance(result_dto, MovieDetailDto)
    assert result_dto.movie_id == 123
    assert result_dto.title_info.korean_title == "테스트 영화"
    assert result_dto.runtime_minutes == 120

    # 이제 이 검증이 성공적으로 통과합니다.
    assert "드라마" in result_dto.genres
    assert "액션" in result_dto.genres


# 계약: get_movie_details 호출 시, 리포지토리가 영화를 찾지 못해 None을 반환하면,
#       서비스 또한 None을 반환해야 한다.
def test_get_movie_details_not_found(mock_repositories):
    # --- 1. 준비 (Arrange) ---
    mock_movie_repo, mock_search_repo = mock_repositories
    # `find_by_id`가 호출되면 None을 반환하도록 설정합니다.
    mock_movie_repo.find_by_id.return_value = None
    service = MovieAppService(mock_movie_repo, mock_search_repo)

    # --- 2. 실행 (Act) ---
    result = service.get_movie_details(movie_id=999)

    # --- 3. 검증 (Assert) ---
    mock_movie_repo.find_by_id.assert_called_once_with(999)
    assert result is None


# --- search_movies 메서드 테스트 ---

# 계약: search_movies 호출 시, 서비스는 주어진 검색 조건을 그대로 검색 리포지토리에 전달하고,
#       리포지토리의 반환 결과를 그대로 반환해야 한다. (서비스는 로직 없이 전달만 책임진다)
def test_search_movies_delegates_to_repository(mock_repositories):
    # --- 1. 준비 (Arrange) ---
    mock_movie_repo, mock_search_repo = mock_repositories

    # 가상의 검색 조건 DTO와 예상 반환 결과를 설정합니다.
    criteria = MovieSearchCriteriaDto(keyword="테스트")
    expected_result = MovieSearchResultDto(movies=[], total_results=0, current_page=1, total_pages=0)
    mock_search_repo.search_movies.return_value = expected_result

    service = MovieAppService(mock_movie_repo, mock_search_repo)

    # --- 2. 실행 (Act) ---
    result = service.search_movies(criteria)

    # --- 3. 검증 (Assert) ---
    # 검색 리포지토리의 search_movies가 올바른 인자로 한 번 호출되었는지 확인합니다.
    mock_search_repo.search_movies.assert_called_once_with(criteria=criteria)
    # 서비스의 반환 값이 리포지토리의 반환 값과 동일한 객체인지 확인합니다.
    assert result is expected_result


# --- get_popular_movies 메서드 테스트 ---

# 계약: get_popular_movies 호출 시, 서비스는 모든 인자를 검색 리포지토리에 올바르게 전달해야 한다.
def test_get_popular_movies_delegates_to_repository_with_all_args(mock_repositories):
    # --- 1. 준비 (Arrange) ---
    mock_movie_repo, mock_search_repo = mock_repositories

    list_type = "top_rated"
    genre = "코미디"
    pagination = PaginationDto(page_number=2, page_size=10)
    expected_result = "some_popular_movie_list"  # 단순 문자열로 대체 가능
    mock_search_repo.find_popular_movies.return_value = expected_result

    service = MovieAppService(mock_movie_repo, mock_search_repo)

    # --- 2. 실행 (Act) ---
    result = service.get_popular_movies(list_type=list_type, genre_filter=genre, pagination_dto=pagination)

    # --- 3. 검증 (Assert) ---
    mock_search_repo.find_popular_movies.assert_called_once_with(
        list_type_criterion=list_type,
        genre_filter=genre,
        pagination=pagination
    )
    assert result is expected_result


# 계약: get_popular_movies 호출 시, 페이지네이션 DTO가 없으면 서비스가 기본 PaginationDto를 생성하여 전달해야 한다.
def test_get_popular_movies_creates_default_pagination(mock_repositories):
    # --- 1. 준비 (Arrange) ---
    mock_movie_repo, mock_search_repo = mock_repositories
    service = MovieAppService(mock_movie_repo, mock_search_repo)

    # --- 2. 실행 (Act) ---
    service.get_popular_movies(list_type="latest")

    # --- 3. 검증 (Assert) ---
    # find_popular_movies가 호출되었는지 확인
    assert mock_search_repo.find_popular_movies.called
    # 호출될 때 pagination 인자가 PaginationDto 타입의 객체였는지 확인
    # call_args는 (args, kwargs) 튜플을 반환
    args, kwargs = mock_search_repo.find_popular_movies.call_args
    assert isinstance(kwargs.get('pagination'), PaginationDto)
    assert kwargs.get('pagination').page_number == 1
    assert kwargs.get('pagination').page_size == 20