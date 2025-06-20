import logging
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from apps.movie.application.dtos import (
    MovieSearchCriteriaDto, FilterOptionsDto, SortOptionDto, PaginationDto, MovieDetailDto
)
from apps.movie.containers import MovieContainer
from src.apps.movie.interface.serializers import (
    MovieSearchQueryParamSerializer,
    MovieSearchResultResponseSerializer,
    MovieDetailResponseSerializer
)

logger = logging.getLogger(__name__)


class MovieDetailAPIView(APIView):
    def get(self, request, movie_id: int):
        # ✅ 메서드 시작 시점에서 컨테이너로부터 서비스 인스턴스를 직접 가져옴
        service = MovieContainer.movie_app_service()

        logger.info(f"MovieDetailAPIView GET request received for movie_id: {movie_id}")
        try:
            movie_detail_dto = service.get_movie_details(movie_id=movie_id)
            if movie_detail_dto:
                serializer = MovieDetailResponseSerializer(movie_detail_dto)
                return Response(serializer.data)

            logger.warning(f"Movie detail service returned None for movie_id: {movie_id}")
            return Response({"error": "영화를 찾을 수 없습니다."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.exception(f"영화 상세 정보 조회 중 오류 발생 movie_id: {movie_id}")
            return Response({"error": "서버 내부 오류"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class MovieSearchAPIView(APIView):
    def get(self, request):
        # ✅ 메서드 시작 시점에서 컨테이너로부터 서비스 인스턴스를 직접 가져옴
        service = MovieContainer.movie_app_service()

        logger.info(f"MovieSearchAPIView GET request received with params: {request.query_params}")

        query_param_serializer = MovieSearchQueryParamSerializer(data=request.query_params)
        if not query_param_serializer.is_valid():
            logger.warning(f"MovieSearchAPIView request validation failed: {query_param_serializer.errors}")
            return Response(query_param_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        validated_data = query_param_serializer.validated_data

        try:
            genres_list = None
            if validated_data.get('genres'):
                genres_list = [genre.strip() for genre in validated_data.get('genres').split(',') if genre.strip()]

            filter_options_dto = FilterOptionsDto(
                genres=genres_list,
                release_year_from=validated_data.get('release_year_from'),
                release_year_to=validated_data.get('release_year_to')
            )

            sort_option_dto = None
            if validated_data.get('sort_field'):
                sort_option_dto = SortOptionDto(
                    field=validated_data.get('sort_field'),
                    direction=validated_data.get('sort_direction', 'desc'),
                    rating_platform=validated_data.get('rating_platform')
                )

            pagination_dto = PaginationDto(
                page_number=validated_data.get('page_number', 1),
                page_size=validated_data.get('page_size', 20)
            )

            criteria_dto = MovieSearchCriteriaDto(
                keyword=validated_data.get('keyword'),
                filters=filter_options_dto,
                sort_by=sort_option_dto,
                pagination=pagination_dto
            )

            search_result_dto = service.search_movies(criteria_dto)
            response_serializer = MovieSearchResultResponseSerializer(search_result_dto)
            return Response(response_serializer.data)
        except (ValueError, TypeError) as e:
            logger.warning(f"영화 검색에 유효하지 않은 데이터입니다.: {e}")
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.exception("MovieSearchAPIView 오류 발생")
            return Response({"error": "영화 검색 중 서버 오류 발생"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class PopularMoviesAPIView(APIView):
    def get(self, request):
        # ✅ 메서드 시작 시점에서 컨테이너로부터 서비스 인스턴스를 직접 가져옴
        service = MovieContainer.movie_app_service()

        logger.info(f"PopularMoviesAPIView GET request with params: {request.query_params}")
        try:
            pagination_dto = PaginationDto(
                page_number=int(request.query_params.get('page_number', 1)),
                page_size=int(request.query_params.get('page_size', 10))
            )
            list_type = request.query_params.get('type', 'latest_highly_rated')
            genre = request.query_params.get('genre')

            popular_movies_dto = service.get_popular_movies(
                list_type=list_type,
                genre_filter=genre,
                pagination_dto=pagination_dto
            )
            response_serializer = MovieSearchResultResponseSerializer(popular_movies_dto)
            return Response(response_serializer.data)
        except (ValueError, TypeError):
            logger.warning(f"Invalid pagination params in PopularMoviesAPIView: {request.query_params}")
            return Response({"error": "잘못된 페이지 또는 페이지 크기 값입니다."}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.exception("An unexpected error occurred in PopularMoviesAPIView.")
            return Response({"error": "인기 영화 목록 조회 중 오류 발생"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)