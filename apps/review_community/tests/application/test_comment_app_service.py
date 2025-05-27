import unittest
from unittest.mock import Mock, MagicMock, patch
from datetime import datetime, timedelta
import uuid

# 테스트 대상 서비스 및 관련 DTO, 도메인 객체 임포트
# 실제 프로젝트에서는 정확한 경로로 수정해야 합니다.
from apps.review_community.application.services import CommentAppService
from apps.review_community.application.dtos import (
    CreateCommentRequestDto, UpdateCommentRequestDto, 
    CommentDto, CommentAuthorDto, CommentListDto, PaginationInfoRequestDto
)
from apps.review_community.domain.aggregates.comment_thread import CommentThread
from apps.review_community.domain.aggregates.comment import Comment
from apps.review_community.domain.value_objects.comment_id_vo import CommentIdVO
from apps.review_community.domain.value_objects.comment_content_vo import CommentContentVO
from apps.review_community.domain.value_objects.author_profile_vo import AuthorProfileVO

# Django의 User 모델 모킹을 위해 (실제 User 모델을 직접 사용해도 되지만, 여기서는 Mock 사용)
# from django.contrib.auth import get_user_model
# User = get_user_model()

class TestCommentAppService(unittest.TestCase):

    def setUp(self):
        self.mock_comment_thread_repository = Mock()
        self.comment_app_service = CommentAppService(
            comment_thread_repository=self.mock_comment_thread_repository
        )
        self.movie_id = 1
        self.author_id = 100
        self.author_nickname = "테스트유저"
        
        self.mock_author_user = Mock()
        self.mock_author_user.pk = self.author_id
        self.mock_author_user.id = self.author_id
        self.mock_author_user.nickname = self.author_nickname
        self.mock_author_user.get_username = Mock(return_value=self.author_nickname)

    def test_add_comment_to_new_thread(self):
        # 계약: 새 영화에 첫 댓글 작성 시, CommentThread가 생성되고 댓글이 추가되어야 한다.
        self.mock_comment_thread_repository.find_by_movie_id.return_value = None
        self.mock_comment_thread_repository.save = MagicMock()
        content_text = "첫 댓글입니다!"
        request_dto = CreateCommentRequestDto(movie_id=self.movie_id, content=content_text)
        
        result_dto = self.comment_app_service.add_comment_to_movie(
            author_user_instance=self.mock_author_user,
            request_dto=request_dto
        )
        self.mock_comment_thread_repository.find_by_movie_id.assert_called_once_with(self.movie_id)
        self.mock_comment_thread_repository.save.assert_called_once()
        saved_thread_arg = self.mock_comment_thread_repository.save.call_args[0][0]
        self.assertIsInstance(saved_thread_arg, CommentThread)
        self.assertEqual(saved_thread_arg.movie_id, self.movie_id)
        self.assertEqual(saved_thread_arg.get_comment_count(), 1)
        self.assertIsInstance(result_dto, CommentDto)
        self.assertEqual(result_dto.content, content_text)

    def test_add_comment_to_existing_thread(self):
        # 계약: 기존 댓글 스레드에 새 댓글을 추가할 수 있어야 한다.
        existing_comment_id = CommentIdVO.generate()
        existing_author_vo = AuthorProfileVO(account_id=99, nickname="이전작성자")
        existing_content_vo = CommentContentVO("이전 댓글")
        existing_comment = Comment(existing_comment_id, existing_content_vo, existing_author_vo, datetime.now())
        
        mock_thread = CommentThread(movie_id=self.movie_id, comments=[existing_comment])
        self.mock_comment_thread_repository.find_by_movie_id.return_value = mock_thread
        self.mock_comment_thread_repository.save = MagicMock()
        new_content_text = "새로운 댓글!"
        request_dto = CreateCommentRequestDto(movie_id=self.movie_id, content=new_content_text)
        
        result_dto = self.comment_app_service.add_comment_to_movie(
            author_user_instance=self.mock_author_user,
            request_dto=request_dto
        )
        self.mock_comment_thread_repository.save.assert_called_once_with(mock_thread)
        self.assertEqual(mock_thread.get_comment_count(), 2)
        newly_added_comment_in_thread = mock_thread.comments[-1]
        self.assertEqual(newly_added_comment_in_thread.content.text, new_content_text)

    def test_get_comments_for_movie_no_comments(self):
        # 계약: 댓글이 없는 영화에 대해 댓글 목록 조회 시, 빈 리스트와 올바른 페이지 정보를 반환해야 한다.
        self.mock_comment_thread_repository.find_by_movie_id.return_value = CommentThread(movie_id=self.movie_id, comments=[])
        pagination_dto = PaginationInfoRequestDto(page=1, page_size=10)
        result_list_dto = self.comment_app_service.get_comments_for_movie(self.movie_id, pagination_dto)
        self.assertEqual(len(result_list_dto.comments), 0)
        self.assertEqual(result_list_dto.total_count, 0)

    def test_get_comments_for_movie_with_pagination(self):
        # 계약: 댓글 목록 조회 시 페이지네이션이 올바르게 적용되어야 한다. (최신순 정렬)
        comments_entities = []
        base_time = datetime.now()
        for i in range(15): # 15개의 댓글 생성 (0~14)
            comment_id = CommentIdVO.generate()
            # 댓글 내용에 순번을 넣어 구분, 최신 댓글이 내용 "댓글 내용 15"가 되도록
            content = CommentContentVO(f"댓글 내용 {15-i}") 
            author = AuthorProfileVO(account_id=i+1, nickname=f"작성자{i+1}")
            # 최신 댓글이 created_at 값이 가장 크도록 생성 (가장 나중에 생성)
            comments_entities.append(Comment(comment_id, content, author, base_time + timedelta(minutes=i)))
        
        # 서비스는 내부적으로 created_at으로 역순 정렬하므로,
        # comments_entities를 그대로 전달해도 서비스에서 정렬됨.
        # 또는 테스트에서 미리 역순 정렬된 리스트를 만들어 전달할 수도 있음.
        # 여기서는 서비스의 정렬 로직을 믿고 그대로 전달.
        mock_thread = CommentThread(movie_id=self.movie_id, comments=comments_entities)
        self.mock_comment_thread_repository.find_by_movie_id.return_value = mock_thread

        pagination_dto_page1 = PaginationInfoRequestDto(page=1, page_size=5)
        result_page1 = self.comment_app_service.get_comments_for_movie(self.movie_id, pagination_dto_page1)
        
        self.assertEqual(len(result_page1.comments), 5)
        self.assertEqual(result_page1.total_count, 15)
        self.assertEqual(result_page1.page, 1)
        self.assertEqual(result_page1.total_pages, 3)
        # 서비스에서 created_at 역순 정렬하므로, 가장 최근에 만들어진 댓글이 첫 번째
        # base_time + timedelta(minutes=14)가 가장 최근 댓글 (내용은 "댓글 내용 1")
        # base_time + timedelta(minutes=0)이 가장 오래된 댓글 (내용은 "댓글 내용 15")
        # 서비스 로직: sorted(comment_thread.comments, key=lambda c: c.created_at, reverse=True)
        # 따라서, result_page1.comments[0]은 comments_entities[14] (내용: "댓글 내용 1") 이어야 함
        self.assertEqual(result_page1.comments[0].content, "댓글 내용 1") 
        self.assertEqual(result_page1.comments[4].content, "댓글 내용 5")


        pagination_dto_page3 = PaginationInfoRequestDto(page=3, page_size=5)
        result_page3 = self.comment_app_service.get_comments_for_movie(self.movie_id, pagination_dto_page3)
        self.assertEqual(len(result_page3.comments), 5)
        # 3페이지의 첫번째 댓글은 comments_entities[4] (내용: "댓글 내용 11")
        self.assertEqual(result_page3.comments[0].content, "댓글 내용 11")
        self.assertEqual(result_page3.comments[4].content, "댓글 내용 15")


    def test_update_own_comment_successfully(self):
        # 계약: 사용자는 자신이 작성한 댓글의 내용을 성공적으로 수정할 수 있어야 한다.
        comment_id_vo = CommentIdVO.generate()
        original_content_vo = CommentContentVO("원본 댓글")
        author_vo = AuthorProfileVO(account_id=self.author_id, nickname=self.author_nickname)
        comment_entity = Comment(comment_id_vo, original_content_vo, author_vo, datetime.now())
        
        mock_thread = CommentThread(movie_id=self.movie_id, comments=[comment_entity])
        self.mock_comment_thread_repository.find_by_movie_id.return_value = mock_thread
        self.mock_comment_thread_repository.save = MagicMock()
        update_request_dto = UpdateCommentRequestDto(content="수정된 댓글입니다.")
        
        result_dto = self.comment_app_service.update_comment(
            movie_id=self.movie_id,
            comment_id_str=str(comment_id_vo.value),
            author_account_id=self.author_id,
            request_dto=update_request_dto
        )
        self.mock_comment_thread_repository.save.assert_called_once_with(mock_thread)
        self.assertIsNotNone(result_dto)
        self.assertEqual(result_dto.content, "수정된 댓글입니다.")

    def test_update_others_comment_raises_permission_error(self):
        # 계약: 다른 사용자의 댓글 수정을 시도하면 PermissionError가 발생해야 한다.
        comment_id_vo = CommentIdVO.generate()
        original_content_vo = CommentContentVO("남의 댓글")
        author1_vo = AuthorProfileVO(account_id=self.author_id, nickname="원작성자") 
        comment_entity = Comment(comment_id_vo, original_content_vo, author1_vo, datetime.now())
        
        mock_thread = CommentThread(movie_id=self.movie_id, comments=[comment_entity])
        self.mock_comment_thread_repository.find_by_movie_id.return_value = mock_thread
        
        update_request_dto = UpdateCommentRequestDto(content="내가 수정할거야")
        other_author_id = self.author_id + 1

        with self.assertRaisesRegex(PermissionError, "자신이 작성한 댓글만 수정할 수 있습니다."):
            self.comment_app_service.update_comment(
                movie_id=self.movie_id,
                comment_id_str=str(comment_id_vo.value),
                author_account_id=other_author_id,
                request_dto=update_request_dto
            )

    def test_delete_own_comment_successfully(self):
        # 계약: 사용자는 자신이 작성한 댓글을 성공적으로 삭제할 수 있어야 한다.
        comment_id_vo = CommentIdVO.generate()
        # 각 테스트에서 필요한 content_vo를 생성
        content_vo_for_delete = CommentContentVO("삭제될 댓글") 
        author_vo = AuthorProfileVO(self.author_id, self.author_nickname)
        comment_entity = Comment(comment_id_vo, content_vo_for_delete, author_vo, datetime.now())
        
        mock_thread = CommentThread(movie_id=self.movie_id, comments=[comment_entity])
        self.mock_comment_thread_repository.find_by_movie_id.return_value = mock_thread
        self.mock_comment_thread_repository.save = MagicMock()
        
        self.comment_app_service.delete_comment(
            movie_id=self.movie_id,
            comment_id_str=str(comment_id_vo.value),
            author_account_id=self.author_id
        )
        self.mock_comment_thread_repository.save.assert_called_once_with(mock_thread)
        self.assertEqual(mock_thread.get_comment_count(), 0)

    def test_delete_others_comment_raises_permission_error(self):
        # 계약: 다른 사용자의 댓글 삭제를 시도하면 PermissionError가 발생해야 한다.
        comment_id_vo = CommentIdVO.generate()
        # 각 테스트에서 필요한 content_vo를 생성
        content_vo_for_other_delete = CommentContentVO("다른 사람 댓글")
        author1_vo = AuthorProfileVO(account_id=self.author_id, nickname="원작성자")
        comment_entity = Comment(comment_id_vo, content_vo_for_other_delete, author1_vo, datetime.now())
        
        mock_thread = CommentThread(movie_id=self.movie_id, comments=[comment_entity])
        self.mock_comment_thread_repository.find_by_movie_id.return_value = mock_thread
        
        other_author_id = self.author_id + 1

        with self.assertRaisesRegex(PermissionError, "자신이 작성한 댓글만 삭제할 수 있습니다."):
            self.comment_app_service.delete_comment(
                movie_id=self.movie_id,
                comment_id_str=str(comment_id_vo.value),
                author_account_id=other_author_id
            )

if __name__ == '__main__':
    unittest.main()