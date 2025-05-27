# 파일 경로: apps/movie/application/services.py
# from typing import List, Optional # 타입 힌트 제거
from datetime import datetime

from django.utils import timezone 

from apps.movie.domain.repositories import MovieRepository, MovieSearchRepository
from apps.movie.domain.aggregates.movie import Movie
from .dtos import (
    MovieSearchCriteriaDto, MovieSearchResultDto, SearchedMovieItemDto,
    MovieDetailDto, TitleInfoDisplayDto, PlotDisplayDto, StillCutDisplayDto,
    TrailerDisplayDto, MoviePlatformRatingDisplayDto, OTTInfoDisplayDto,
    PaginationDto, FilterOptionsDto, SortOptionDto 
)

class MovieAppService:
    def __init__(self, 
                 movie_repository, 
                 movie_search_repository):
        self.movie_repository = movie_repository
        self.movie_search_repository = movie_search_repository

    def _movie_aggregate_to_detail_dto(self, movie):
        genres_display = [genre_vo.name for genre_vo in movie.genres]
        directors_display = [director_vo.name for director_vo in movie.directors]
        cast_display = [
            f"{actor_vo.name}{' (' + actor_vo.role_name + ')' if actor_vo.role_name else ''}" 
            for actor_vo in movie.cast
        ]
        still_cuts_display = [
            StillCutDisplayDto(
                image_url=sc.image_url, 
                caption=sc.caption, 
                display_order=sc.display_order
            ) for sc in movie.still_cuts
        ]
        trailers_display = [
            TrailerDisplayDto(
                url=t.url, 
                trailer_type=t.trailer_type, 
                site_name=t.site_name,
                thumbnail_url=t.thumbnail_url
            ) for t in movie.trailers
        ]
        platform_ratings_display = [
            MoviePlatformRatingDisplayDto(
                platform_name=r.platform_name,
                score=r.score
            ) for r in movie.platform_ratings
        ]
        ott_availability_display = [
            OTTInfoDisplayDto(
                platform_name=o.platform_name,
                watch_url=o.watch_url,
                logo_image_url=o.logo_image_url,
                availability_note=o.availability_note
            ) for o in movie.ott_availability
        ]
        
        title_info_dto = TitleInfoDisplayDto(
            korean_title=movie.title_info.korean_title if movie.title_info else "제목 정보 없음",
            original_title=movie.title_info.original_title if movie.title_info else None
        )
        plot_dto = PlotDisplayDto(text=movie.plot.text if movie.plot else None)
        
        release_date_str_val = movie.release_date.formatted() if movie.release_date else "정보 없음"
        runtime_minutes_val = movie.runtime.minutes if movie.runtime else 0
        poster_image_url_val = movie.poster_image.url if movie.poster_image else ""
        
        created_at_str_val = movie.created_at.isoformat() if movie.created_at else "정보 없음"
        updated_at_str_val = movie.updated_at.isoformat() if movie.updated_at else None

        return MovieDetailDto(
            movie_id=movie.movie_id,
            title_info=title_info_dto,
            plot=plot_dto,
            release_date_str=release_date_str_val,
            runtime_minutes=runtime_minutes_val,
            poster_image_url=poster_image_url_val,
            genres=genres_display,
            directors=directors_display,
            cast=cast_display,
            still_cuts=still_cuts_display,
            trailers=trailers_display,
            platform_ratings=platform_ratings_display,
            ott_availability=ott_availability_display,
            created_at_str=created_at_str_val,
            updated_at_str=updated_at_str_val
        )

    def search_movies(self, criteria_dto):
        return self.movie_search_repository.search_movies(criteria=criteria_dto)

    def get_movie_details(self, movie_id):
        movie_aggregate = self.movie_repository.find_by_id(movie_id)
        if not movie_aggregate:
            return None
        
        movie_detail_dto = self._movie_aggregate_to_detail_dto(movie_aggregate)
        return movie_detail_dto

    def get_popular_movies(self, 
                           list_type, 
                           genre_filter=None, 
                           pagination_dto=None
                          ):
        
        resolved_pagination = pagination_dto if pagination_dto else PaginationDto()
        return self.movie_search_repository.find_popular_movies(
            list_type_criterion=list_type,
            genre_filter=genre_filter,
            pagination=resolved_pagination
        )