# 파일 경로: apps/movie/domain/repositories.py
import abc
# from typing import List, Optional # 타입 힌트 제거
from .aggregates.movie import Movie 
from apps.movie.application.dtos import MovieSearchCriteriaDto, MovieSearchResultDto, PaginationDto

class MovieRepository(abc.ABC):
    @abc.abstractmethod
    def find_by_id(self, movie_id):
        raise NotImplementedError

    @abc.abstractmethod
    def save(self, movie):
        raise NotImplementedError

    @abc.abstractmethod
    def delete(self, movie_id):
        raise NotImplementedError

class MovieSearchRepository(abc.ABC):
    @abc.abstractmethod
    def search_movies(self, criteria):
        raise NotImplementedError

    @abc.abstractmethod
    def find_popular_movies(self, 
                              list_type_criterion,
                              genre_filter,
                              pagination
                             ):
        raise NotImplementedError