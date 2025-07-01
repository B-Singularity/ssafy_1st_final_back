import abc
from .aggregates.comment_thread import CommentThread
from .value_objects.comment_id_vo import CommentIdVO

class CommentThreadRepository(abc.ABC):
    @abc.abstractmethod
    def find_by_movie_id(self, movie_id):
        raise NotImplementedError

    @abc.abstractmethod
    def save(self, comment_thread):
        raise NotImplementedError