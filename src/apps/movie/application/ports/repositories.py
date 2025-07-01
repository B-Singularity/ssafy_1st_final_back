import abc

from src.apps.movie.domain.aggregates.movie import Movie


class MovieRepository(abc.ABC):
    @abc.abstractmethod
    def find_by_id(self, movie_id):
        raise NotImplementedError

    @abc.abstractmethod
    def save(self, movie: Movie):
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


