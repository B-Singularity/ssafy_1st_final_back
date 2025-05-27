from datetime import datetime

from apps.review_community.domain.aggregates.comment import Comment
from apps.review_community.domain.value_objects.comment_id_vo import CommentIdVO
from apps.review_community.domain.value_objects.comment_content_vo import CommentContentVO
from apps.review_community.domain.value_objects.author_profile_vo import AuthorProfileVO


class CommentThread: 
    def __init__(self, movie_id, comments=None):
        if not isinstance(movie_id, int) or movie_id <= 0:
            raise ValueError("영화 ID는 0보다 큰 정수여야 합니다.")
        
        self._movie_id = movie_id
        self._comments = [] 
        if comments:
            for comment_entity in comments:
                if not isinstance(comment_entity, Comment):
                    raise TypeError("댓글 목록에는 Comment 엔티티만 포함될 수 있습니다.")
                self._comments.append(comment_entity)

    @property
    def movie_id(self):
        return self._movie_id

    @property
    def comments(self):
        return list(self._comments)

    def add_comment(self, author, content):
        new_comment_id = CommentIdVO.generate()
        now = datetime.now()
        
        new_comment = Comment(
            comment_id=new_comment_id,
            content=content,
            author=author,
            created_at=now
        )
        self._comments.append(new_comment)
        return new_comment

    def find_comment_by_id(self, comment_id_to_find):
        if not isinstance(comment_id_to_find, CommentIdVO):
            raise TypeError("comment_id_to_find는 CommentIdVO의 인스턴스여야 합니다.")
        for comment in self._comments:
            if comment.comment_id == comment_id_to_find:
                return comment
        return None

    def update_comment_content(self, comment_id_to_update, new_content, author_id_making_change):
        comment_to_update = self.find_comment_by_id(comment_id_to_update)
        if not comment_to_update:
            raise ValueError("수정하려는 댓글을 찾을 수 없습니다.")
        
        if comment_to_update.author.account_id != author_id_making_change:
            raise PermissionError("자신이 작성한 댓글만 수정할 수 있습니다.")
            
        comment_to_update.update_content(new_content)

    def delete_comment(self, comment_id_to_delete, author_id_making_change):
        comment_to_delete = self.find_comment_by_id(comment_id_to_delete)
        if not comment_to_delete: 
            return

        if comment_to_delete.author.account_id != author_id_making_change:
            raise PermissionError("자신이 작성한 댓글만 삭제할 수 있습니다.")
            
        self._comments.remove(comment_to_delete)

    def get_comment_count(self):
        return len(self._comments)

    def __eq__(self, other):
        if not isinstance(other, CommentThread):
            return NotImplemented
        return self._movie_id == other._movie_id

    def __hash__(self):
        return hash(self._movie_id)