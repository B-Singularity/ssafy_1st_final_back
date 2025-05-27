import unittest
from datetime import datetime, timedelta
from apps.review_community.domain.aggregates.comment import Comment
from apps.review_community.domain.value_objects.comment_id_vo import CommentIdVO
from apps.review_community.domain.value_objects.comment_content_vo import CommentContentVO
from apps.review_community.domain.value_objects.author_profile_vo import AuthorProfileVO

import uuid

class TestCommentEntity(unittest.TestCase):

    def setUp(self):
        self.author = AuthorProfileVO(account_id=1, nickname="테스트유저")
        self.content = CommentContentVO("이것은 테스트 댓글입니다.")
        self.comment_id = CommentIdVO.generate()
        self.now = datetime.now()

    def test_create_valid_comment(self):
        # 계약: 유효한 값들로 Comment 엔티티를 성공적으로 생성할 수 있어야 한다.
        comment = Comment(
            comment_id=self.comment_id,
            content=self.content,
            author=self.author,
            created_at=self.now
        )
        self.assertIsInstance(comment, Comment)
        self.assertEqual(comment.comment_id, self.comment_id)
        self.assertEqual(comment.content, self.content)
        self.assertEqual(comment.author, self.author)
        self.assertEqual(comment.created_at, self.now)
        self.assertEqual(comment.modified_at, self.now)

    def test_update_content_changes_content_and_modified_at(self):
        # 계약: update_content 메서드는 댓글 내용을 변경하고 modified_at을 갱신해야 한다.
        comment = Comment(self.comment_id, self.content, self.author, self.now)
        old_modified_at = comment.modified_at
        
        new_content_text = "수정된 댓글 내용입니다."
        new_content_vo = CommentContentVO(new_content_text)
        
        # import time; time.sleep(0.001) # 수정 시간 차이를 위한 미세한 대기
        
        comment.update_content(new_content_vo)
        
        self.assertEqual(comment.content, new_content_vo)
        self.assertTrue(comment.modified_at > old_modified_at)

    def test_update_content_with_same_content_does_not_change_modified_at(self):
        # 계약: 동일한 내용으로 업데이트 시 modified_at은 변경되지 않아야 한다.
        comment = Comment(self.comment_id, self.content, self.author, self.now)
        original_modified_at = comment.modified_at
        
        comment.update_content(self.content)
        self.assertEqual(comment.modified_at, original_modified_at)

    def test_comment_equality_based_on_id(self):
        # 계약: 두 Comment 엔티티는 comment_id가 같으면 동등해야 한다.
        id1 = CommentIdVO.generate()
        id2 = CommentIdVO.generate()
        content1 = CommentContentVO("내용1")
        content2 = CommentContentVO("내용2")
        author1 = AuthorProfileVO(1, "작가1")
        now = datetime.now()

        comment1 = Comment(id1, content1, author1, now)
        comment2_same_id = Comment(id1, content2, author1, now) # 내용은 다르지만 ID는 같음
        comment3_diff_id = Comment(id2, content1, author1, now)

        self.assertEqual(comment1, comment2_same_id)
        self.assertNotEqual(comment1, comment3_diff_id)

    def test_comment_hash_consistency(self):
        # 계약: 동등한 Comment 엔티티는 동일한 해시 값을 가져야 한다.
        id1 = CommentIdVO.generate()
        content1 = CommentContentVO("내용1")
        author1 = AuthorProfileVO(1, "작가1")
        now = datetime.now()

        comment1 = Comment(id1, content1, author1, now)
        comment2_same_id = Comment(id1, CommentContentVO("다른내용"), author1, now)
        self.assertEqual(hash(comment1), hash(comment2_same_id))

    def test_string_representation(self):
        # 계약: Comment 엔티티의 문자열 표현은 댓글 내용이어야 한다.
        comment = Comment(self.comment_id, self.content, self.author, self.now)
        self.assertEqual(str(comment), self.content.text)

if __name__ == '__main__':
    unittest.main()