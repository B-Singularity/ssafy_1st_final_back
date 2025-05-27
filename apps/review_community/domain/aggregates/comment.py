from datetime import datetime
from apps.review_community.domain.value_objects.comment_id_vo import CommentIdVO
from apps.review_community.domain.value_objects.comment_content_vo import CommentContentVO
from apps.review_community.domain.value_objects.author_profile_vo import AuthorProfileVO

class Comment:
    def __init__(self,
                 comment_id, 
                 content,    
                 author,     
                 created_at, 
                 modified_at=None): 
        
        if not isinstance(comment_id, CommentIdVO):
            raise TypeError("comment_id는 CommentIdVO의 인스턴스여야 합니다.")
        if not isinstance(content, CommentContentVO):
            raise TypeError("content는 CommentContentVO의 인스턴스여야 합니다.")
        if not isinstance(author, AuthorProfileVO):
            raise TypeError("author는 AuthorProfileVO의 인스턴스여야 합니다.")
        if not isinstance(created_at, datetime):
            raise TypeError("created_at은 datetime 객체여야 합니다.")
        if modified_at is not None and not isinstance(modified_at, datetime):
            raise TypeError("modified_at이 None이 아니면 datetime 객체여야 합니다.")

        self._comment_id = comment_id
        self._content = content
        self._author = author
        self._created_at = created_at
        self._modified_at = modified_at if modified_at else created_at 

    @property
    def comment_id(self):
        return self._comment_id

    @property
    def content(self):
        return self._content

    @property
    def author(self):
        return self._author

    @property
    def created_at(self):
        return self._created_at

    @property
    def modified_at(self):
        return self._modified_at
        
    def update_content(self, new_content):
        if not isinstance(new_content, CommentContentVO):
            raise TypeError("새로운 댓글 내용은 CommentContentVO의 인스턴스여야 합니다.")
        if self._content == new_content:
            return 
        self._content = new_content
        self._modified_at = datetime.now() 

    def __eq__(self, other):
        if not isinstance(other, Comment):
            return NotImplemented
        return self._comment_id == other._comment_id

    def __hash__(self):
        return hash(self._comment_id)

    def __str__(self):
        return str(self._content.text if self._content else "")