from datetime import datetime

class CreateCommentRequestDto:
    def __init__(self, movie_id, content):
        if not movie_id or movie_id <= 0:
            raise ValueError("유효한 영화 ID가 필요합니다.")
        if not content or not (1 <= len(content.strip()) <= 500):
            raise ValueError("댓글 내용은 1자 이상 500자 이하이어야 합니다.")
        self.movie_id = movie_id
        self.content = content.strip()

class UpdateCommentRequestDto:
    def __init__(self, content):
        if not content or not (1 <= len(content.strip()) <= 500):
            raise ValueError("댓글 내용은 1자 이상 500자 이하이어야 합니다.")
        self.content = content.strip()

class CommentAuthorDto:
    def __init__(self, account_id, nickname):
        self.account_id = account_id
        self.nickname = nickname

class CommentDto:
    def __init__(self, 
                 comment_id,
                 movie_id,
                 author,
                 content,
                 created_at,
                 modified_at):
        self.comment_id = comment_id
        self.movie_id = movie_id
        self.author = author
        self.content = content
        self.created_at = created_at
        self.modified_at = modified_at

class CommentListDto:
    def __init__(self, 
                 comments, 
                 total_count, 
                 page, 
                 page_size):
        self.comments = comments
        self.total_count = total_count
        self.page = page
        self.page_size = page_size
        self.total_pages = (total_count + page_size - 1) // page_size if page_size > 0 else 0

class PaginationInfoRequestDto: 
    def __init__(self, page = 1, page_size = 10):
        if not isinstance(page, int) or page < 1:
            raise ValueError("페이지 번호는 1 이상의 정수여야 합니다.")
        if not isinstance(page_size, int) or not (1 <= page_size <= 50):
            raise ValueError("페이지 크기는 1에서 50 사이의 정수여야 합니다.")
        self.page = page
        self.page_size = page_size