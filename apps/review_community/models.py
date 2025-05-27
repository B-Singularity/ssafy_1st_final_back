from django.db import models
import uuid
from django.conf import settings
from apps.movie.models import MovieModel

class CommentModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    # ⭐️ movie_id 필드를 ForeignKey로 변경
    movie = models.ForeignKey(
        'movie.MovieModel', # '앱이름.모델이름' 형식으로 문자열 참조 또는 직접 임포트
        on_delete=models.CASCADE, 
        related_name="comments_on_movie" # MovieModel에서 이 댓글들을 참조할 때 사용할 이름
    )

    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name="comments_by_author"
    )
    
    content = models.TextField(max_length=500) 
    
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "movie_comments"
        ordering = ['-created_at']
        verbose_name = "영화 댓글"
        verbose_name_plural = "영화 댓글 목록"

    def __str__(self):
        author_display = self.author_id 
        if hasattr(self.author, 'nickname'):
            author_display = self.author.nickname
        elif hasattr(self.author, 'email_address'):
            author_display = self.author.email_address
        
        movie_title = self.movie_id # 기본적으로 movie의 PK 표시
        if hasattr(self.movie, 'korean_title'): # MovieModel에 korean_title 필드가 있다고 가정
            movie_title = self.movie.korean_title
            
        return f"Comment by {author_display} on movie '{movie_title}': {self.content[:30]}"