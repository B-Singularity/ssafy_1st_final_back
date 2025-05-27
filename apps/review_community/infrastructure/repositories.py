from django.db import transaction
from django.contrib.auth import get_user_model
import uuid

from apps.review_community.domain.aggregates.comment_thread import CommentThread
from apps.review_community.domain.aggregates.comment import Comment
from apps.review_community.domain.value_objects.comment_id_vo import CommentIdVO
from apps.review_community.domain.value_objects.comment_content_vo import CommentContentVO
from apps.review_community.domain.value_objects.author_profile_vo import AuthorProfileVO
from apps.review_community.domain.repositories import CommentThreadRepository
from apps.review_community.models import CommentModel

User = get_user_model()


class DjangoCommentThreadRepository(CommentThreadRepository):
    def _to_comment_entity(self, comment_model):
        author_vo = AuthorProfileVO(
            account_id=comment_model.author.pk,
            nickname=getattr(comment_model.author, 'nickname', str(comment_model.author))
        )
        return Comment(
            comment_id=CommentIdVO(str(comment_model.id)),
            content=CommentContentVO(comment_model.content),
            author=author_vo,
            created_at=comment_model.created_at,
            modified_at=comment_model.modified_at
        )

    def find_by_movie_id(self, movie_id):
        comment_models = CommentModel.objects.filter(movie_id=movie_id).select_related('author').order_by('created_at')
        
        comments_entities = [self._to_comment_entity(cm) for cm in comment_models]
        return CommentThread(movie_id=movie_id, comments=comments_entities)

    @transaction.atomic
    def save(self, comment_thread):
        existing_comment_ids_in_db = set(
            CommentModel.objects.filter(movie_id=comment_thread.movie_id).values_list('id', flat=True)
        )
        
        current_comment_ids_in_aggregate = set()

        for comment_entity in comment_thread.comments:
            comment_id_uuid = uuid.UUID(comment_entity.comment_id.value)
            current_comment_ids_in_aggregate.add(comment_id_uuid)
            
            author_instance = User.objects.get(pk=comment_entity.author.account_id)

            CommentModel.objects.update_or_create(
                id=comment_id_uuid,
                movie_id=comment_thread.movie_id,
                defaults={
                    'author': author_instance,
                    'content': comment_entity.content.text,
                    'created_at': comment_entity.created_at,
                    'modified_at': comment_entity.modified_at
                }
            )
        
        ids_to_delete = existing_comment_ids_in_db - current_comment_ids_in_aggregate
        if ids_to_delete:
            CommentModel.objects.filter(id__in=ids_to_delete, movie_id=comment_thread.movie_id).delete()