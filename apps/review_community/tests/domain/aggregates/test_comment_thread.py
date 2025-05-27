import unittest
from datetime import datetime, timedelta
import uuid

from apps.review_community.domain.aggregates.comment_thread import CommentThread
from apps.review_community.domain.aggregates.comment import Comment
from apps.review_community.domain.value_objects.comment_id_vo import CommentIdVO
from apps.review_community.domain.value_objects.comment_content_vo import CommentContentVO
from apps.review_community.domain.value_objects.author_profile_vo import AuthorProfileVO


class TestCommentThreadAggregate(unittest.TestCase):

    def setUp(self):
        self.movie_id = 123
        self.author1 = AuthorProfileVO(account_id=1, nickname="작성자1")
        self.author2 = AuthorProfileVO(account_id=2, nickname="작성자2")
        self.content_vo1 = CommentContentVO("첫 번째 댓글 내용입니다.")
        self.content_vo2 = CommentContentVO("두 번째 댓글 내용입니다.")

    def test_create_empty_comment_thread(self):
        # 계약: 유효한 movie_id로 비어있는 CommentThread를 생성할 수 있어야 한다.
        thread = CommentThread(movie_id=self.movie_id)
        self.assertEqual(thread.movie_id, self.movie_id)
        self.assertEqual(thread.get_comment_count(), 0)
        self.assertEqual(len(thread.comments), 0)

    def test_create_comment_thread_with_initial_comments(self):
        # 계약: 초기 댓글 목록을 가지고 CommentThread를 생성할 수 있어야 한다.
        comment_id1 = CommentIdVO.generate()
        comment1 = Comment(comment_id1, self.content_vo1, self.author1, datetime.now())
        thread = CommentThread(movie_id=self.movie_id, comments=[comment1])
        self.assertEqual(thread.get_comment_count(), 1)
        self.assertIn(comment1, thread.comments)

    def test_add_comment_to_thread(self):
        # 계약: CommentThread에 새로운 댓글을 추가할 수 있어야 한다.
        # 계약: 추가된 댓글은 comments 리스트에 포함되어야 하고, count가 증가해야 한다.
        thread = CommentThread(movie_id=self.movie_id)
        added_comment = thread.add_comment(author=self.author1, content=self.content_vo1)
        
        self.assertEqual(thread.get_comment_count(), 1)
        self.assertIn(added_comment, thread.comments)
        self.assertEqual(added_comment.author, self.author1)
        self.assertEqual(added_comment.content, self.content_vo1)
        self.assertIsInstance(added_comment.comment_id, CommentIdVO)
        self.assertIsNotNone(added_comment.created_at)

    def test_find_comment_by_id(self):
        # 계약: 추가된 댓글을 ID로 찾을 수 있어야 한다. 없는 ID로는 None을 반환해야 한다.
        thread = CommentThread(movie_id=self.movie_id)
        comment1 = thread.add_comment(author=self.author1, content=self.content_vo1)
        thread.add_comment(author=self.author2, content=self.content_vo2) # 다른 댓글 추가

        found_comment1 = thread.find_comment_by_id(comment1.comment_id)
        self.assertIsNotNone(found_comment1)
        self.assertEqual(found_comment1.comment_id, comment1.comment_id)
        self.assertEqual(found_comment1, comment1) # __eq__ 메서드 동작 확인
        
        non_existent_id_vo = CommentIdVO.generate()
        found_comment_none = thread.find_comment_by_id(non_existent_id_vo)
        self.assertIsNone(found_comment_none)

    def test_update_comment_content_by_author(self):
        # 계약: 댓글 작성자는 자신의 댓글 내용을 수정할 수 있어야 한다.
        thread = CommentThread(movie_id=self.movie_id)
        comment_to_update = thread.add_comment(author=self.author1, content=self.content_vo1)
        
        new_content_text = "수정된 댓글 내용입니다!"
        new_content_vo = CommentContentVO(new_content_text)
        
        original_modified_at = comment_to_update.modified_at
        # 수정 시간의 명확한 차이를 위해 잠시 대기 (실제 테스트에서는 불필요하거나 모킹 사용)
        # import time; time.sleep(0.001) 

        thread.update_comment_content(comment_to_update.comment_id, new_content_vo, self.author1.account_id)
        
        # 수정된 댓글 객체를 다시 찾아 확인
        updated_comment_in_thread = thread.find_comment_by_id(comment_to_update.comment_id)
        self.assertIsNotNone(updated_comment_in_thread)
        self.assertEqual(updated_comment_in_thread.content.text, new_content_text)
        self.assertTrue(updated_comment_in_thread.modified_at > original_modified_at)

    def test_update_comment_content_by_other_user_raises_permission_error(self):
        # 계약: 댓글 작성자가 아닌 다른 사용자가 수정 시도 시 PermissionError가 발생해야 한다.
        thread = CommentThread(movie_id=self.movie_id)
        comment_to_update = thread.add_comment(author=self.author1, content=self.content_vo1)
        new_content_vo = CommentContentVO("다른 사용자가 수정 시도")

        with self.assertRaisesRegex(PermissionError, "자신이 작성한 댓글만 수정할 수 있습니다."):
            thread.update_comment_content(comment_to_update.comment_id, new_content_vo, self.author2.account_id)

    def test_update_non_existent_comment_raises_value_error(self):
        # 계약: 존재하지 않는 댓글 수정 시도 시 ValueError가 발생해야 한다.
        thread = CommentThread(movie_id=self.movie_id)
        non_existent_id = CommentIdVO.generate()
        new_content_vo = CommentContentVO("내용")
        with self.assertRaisesRegex(ValueError, "수정하려는 댓글을 찾을 수 없습니다."):
            thread.update_comment_content(non_existent_id, new_content_vo, self.author1.account_id)


    def test_delete_comment_by_author(self):
        # 계약: 댓글 작성자는 자신의 댓글을 삭제할 수 있어야 한다.
        thread = CommentThread(movie_id=self.movie_id)
        comment1 = thread.add_comment(author=self.author1, content=self.content_vo1)
        comment2 = thread.add_comment(author=self.author2, content=self.content_vo2)
        
        self.assertEqual(thread.get_comment_count(), 2)
        thread.delete_comment(comment1.comment_id, self.author1.account_id)
        self.assertEqual(thread.get_comment_count(), 1)
        self.assertIsNone(thread.find_comment_by_id(comment1.comment_id))
        self.assertIsNotNone(thread.find_comment_by_id(comment2.comment_id))

    def test_delete_comment_by_other_user_raises_permission_error(self):
        # 계약: 댓글 작성자가 아닌 다른 사용자가 삭제 시도 시 PermissionError가 발생해야 한다.
        thread = CommentThread(movie_id=self.movie_id)
        comment_to_delete = thread.add_comment(author=self.author1, content=self.content_vo1)

        with self.assertRaisesRegex(PermissionError, "자신이 작성한 댓글만 삭제할 수 있습니다."):
            thread.delete_comment(comment_to_delete.comment_id, self.author2.account_id)
        self.assertEqual(thread.get_comment_count(), 1) 

    def test_delete_non_existent_comment_does_not_raise_error(self):
        # 계약: 존재하지 않는 댓글 삭제 시도 시 오류 없이 조용히 처리되어야 한다.
        thread = CommentThread(movie_id=self.movie_id)
        non_existent_id = CommentIdVO.generate()
        try:
            thread.delete_comment(non_existent_id, self.author1.account_id)
            self.assertEqual(thread.get_comment_count(), 0) 
        except Exception as e:
            self.fail(f"존재하지 않는 댓글 삭제 시 예외 발생: {e}")

    def test_comment_thread_equality(self):
        # 계약: 두 CommentThread 애그리게이트는 movie_id가 같으면 동등해야 한다.
        thread1 = CommentThread(movie_id=123)
        thread2 = CommentThread(movie_id=123)
        thread3 = CommentThread(movie_id=456)

        self.assertEqual(thread1, thread2)
        self.assertNotEqual(thread1, thread3)

    def test_comment_thread_hash_consistency(self):
        # 계약: 동등한 CommentThread 애그리게이트는 동일한 해시 값을 가져야 한다.
        thread1 = CommentThread(movie_id=789)
        thread2 = CommentThread(movie_id=789)
        self.assertEqual(hash(thread1), hash(thread2))

if __name__ == '__main__':
    unittest.main()