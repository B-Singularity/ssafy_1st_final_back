import pytest
from unittest.mock import MagicMock
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

from apps.movie.application.dtos import MovieDetailDto, SearchedMovieItemDto, MovieSearchResultDto, TitleInfoDisplayDto, \
    PlotDisplayDto
from apps.movie.containers import MovieContainer

pytestmark = pytest.mark.django_db


@pytest.fixture
def api_client():
    return APIClient()


# Mocking을 전담하는 새로운 픽스처 생성
@pytest.fixture
def mock_movie_service():
    mock_service = MagicMock()
    with MovieContainer.movie_app_service.override(mock_service):
        yield mock_service


# --- 이제 모든 테스트는 'mocker' 대신 'mock_movie_service' 픽스처를 사용합니다. ---

def test_movie_detail_view_success(api_client, mock_movie_service):
    # --- 준비 (Arrange) ---
    mock_service_instance = MagicMock()
    mock_dto = MagicMock(spec=MovieDetailDto)

    # ✅ Serializer가 필요로 하는 모든 속성을 mock_dto에 설정합니다.
    mock_dto.movie_id = 123
    mock_dto.title_info = MagicMock(spec=TitleInfoDisplayDto)
    mock_dto.title_info.korean_title = "상세정보 테스트 영화"
    mock_dto.title_info.original_title = "Detail Test Movie"

    mock_dto.plot = MagicMock(spec=PlotDisplayDto)
    mock_dto.plot.text = "이것은 줄거리입니다."

    mock_dto.release_date_str = "2025-01-01"
    mock_dto.runtime_minutes = 130
    mock_dto.poster_image_url = "http://example.com/poster.jpg"
    mock_dto.genres = ["드라마", "스릴러"]
    mock_dto.directors = ["김감독"]
    mock_dto.cast = ["박배우 (주연)"]
    mock_dto.still_cuts = []
    mock_dto.trailers = []
    mock_dto.platform_ratings = []
    mock_dto.ott_availability = []
    mock_dto.created_at_str = "2025-01-01T00:00:00"
    mock_dto.updated_at_str = "2025-01-01T00:00:00"

    # mock 서비스가 이 완전한 mock_dto를 반환하도록 설정합니다.
    mock_service_instance.get_movie_details.return_value = mock_dto

    # 컨테이너의 provider를 override 합니다.
    with MovieContainer.movie_app_service.override(mock_service_instance):
        url = reverse('movie_detail', kwargs={'movie_id': 123})
        response = api_client.get(url)

    # --- 검증 (Assert) ---
    assert response.status_code == status.HTTP_200_OK
    mock_service_instance.get_movie_details.assert_called_once_with(movie_id=123)
    assert response.data['movie_id'] == 123
    assert response.data['plot']['text'] == "이것은 줄거리입니다."

def test_movie_detail_view_not_found(api_client, mock_movie_service):
    # --- 준비 (Arrange) ---
    mock_movie_service.get_movie_details.return_value = None

    # --- 실행 (Act) ---
    url = reverse('movie_detail', kwargs={'movie_id': 999})
    response = api_client.get(url)

    # --- 검증 (Assert) ---
    assert response.status_code == status.HTTP_404_NOT_FOUND
    mock_movie_service.get_movie_details.assert_called_once_with(movie_id=999)


def test_movie_search_view_success(api_client, mock_movie_service):
    # --- 준비 (Arrange) ---
    mock_result_dto = MagicMock(spec=MovieSearchResultDto)
    mock_result_dto.movies = []
    mock_result_dto.total_results = 0
    mock_result_dto.current_page = 1
    mock_result_dto.total_pages = 0

    mock_movie_service.search_movies.return_value = mock_result_dto

    # --- 실행 (Act) ---
    url = reverse('movie_search')
    response = api_client.get(f"{url}?keyword=테스트")

    # --- 검증 (Assert) ---
    assert response.status_code == status.HTTP_200_OK
    mock_movie_service.search_movies.assert_called_once()