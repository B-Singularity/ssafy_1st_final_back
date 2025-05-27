from datetime import datetime
import uuid

from django.core.paginator import Paginator
from django.contrib.auth import get_user_model

from apps.review_community.domain.repositories import CommentThreadRepository
from apps.review_community.domain.aggregates.comment_thread import CommentThread
from apps.review_community.domain.aggregates.comment import Comment
from apps.review_community.domain.value_objects.comment_id_vo import CommentIdVO
from apps.review_community.domain.value_objects.comment_content_vo import CommentContentVO
from apps.review_community.domain.value_objects.author_profile_vo import AuthorProfileVO
from apps.review_community.application.dtos import CreateCommentRequestDto, UpdateCommentRequestDto, CommentDto, CommentAuthorDto, CommentListDto, PaginationInfoRequestDto

User = get_user_model()

class CommentAppService:
    def __init__(self, 
                 comment_thread_repository):
        self.comment_thread_repository = comment_thread_repository

    def _map_comment_entity_to_dto_with_movie_id(self, comment_entity, movie_id):
        author_dto = CommentAuthorDto(
            account_id=comment_entity.author.account_id,
            nickname=comment_entity.author.nickname
        )
        return CommentDto(
            comment_id=str(comment_entity.comment_id.value),
            movie_id=movie_id,
            author=author_dto,
            content=comment_entity.content.text,
            created_at=comment_entity.created_at,
            modified_at=comment_entity.modified_at
        )

    def add_comment_to_movie(self, author_user_instance, request_dto):
        comment_thread = self.comment_thread_repository.find_by_movie_id(request_dto.movie_id)
        if not comment_thread:
            comment_thread = CommentThread(movie_id=request_dto.movie_id)

        author_vo = AuthorProfileVO(
            account_id=author_user_instance.pk, 
            nickname=getattr(author_user_instance, 'nickname', str(author_user_instance)) 
        )
        content_vo = CommentContentVO(request_dto.content)
        
        new_comment_entity = comment_thread.add_comment(author=author_vo, content=content_vo)
        self.comment_thread_repository.save(comment_thread)
        
        return self._map_comment_entity_to_dto_with_movie_id(new_comment_entity, request_dto.movie_id)

    def get_comments_for_movie(self, movie_id, pagination_request_dto):
        comment_thread = self.comment_thread_repository.find_by_movie_id(movie_id)
        if not comment_thread:
            return CommentListDto(comments=[], total_count=0, page=pagination_request_dto.page, page_size=pagination_request_dto.page_size)

        all_comments = sorted(comment_thread.comments, key=lambda c: c.created_at, reverse=True)
        
        paginator = Paginator(all_comments, pagination_request_dto.page_size)
        page_obj = paginator.get_page(pagination_request_dto.page)
        
        comment_dtos = [self._map_comment_entity_to_dto_with_movie_id(comment_entity, movie_id) for comment_entity in page_obj.object_list]
        
        return CommentListDto(
            comments=comment_dtos,
            total_count=paginator.count,
            page=page_obj.number,
            page_size=pagination_request_dto.page_size
        )

    def update_comment(self, movie_id, comment_id_str, author_account_id, request_dto):
        comment_thread = self.comment_thread_repository.find_by_movie_id(movie_id)
        if not comment_thread:
            raise ValueError("해당 영화의 댓글 스레드를 찾을 수 없습니다.")

        comment_id_vo = CommentIdVO(comment_id_str)
        new_content_vo = CommentContentVO(request_dto.content)
        
        comment_thread.update_comment_content(comment_id_vo, new_content_vo, author_account_id)
        self.comment_thread_repository.save(comment_thread)
        updated_comment_entity = comment_thread.find_comment_by_id(comment_id_vo)
        if updated_comment_entity:
            return self._map_comment_entity_to_dto_with_movie_id(updated_comment_entity, movie_id)
        return None

    def delete_comment(self, movie_id, comment_id_str, author_account_id):
        comment_thread = self.comment_thread_repository.find_by_movie_id(movie_id)
        if not comment_thread:
            return 

        comment_id_vo = CommentIdVO(comment_id_str)
        comment_thread.delete_comment(comment_id_vo, author_account_id)
        self.comment_thread_repository.save(comment_thread)