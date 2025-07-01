from rest_framework import serializers

class CommentAuthorResponseSerializer(serializers.Serializer):
    account_id = serializers.IntegerField(read_only=True)
    nickname = serializers.CharField(read_only=True)

class CommentResponseSerializer(serializers.Serializer):
    comment_id = serializers.UUIDField(read_only=True)
    movie_id = serializers.IntegerField(read_only=True)
    author = CommentAuthorResponseSerializer(read_only=True)
    content = serializers.CharField(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)
    modified_at = serializers.DateTimeField(read_only=True)

class CreateCommentRequestSerializer(serializers.Serializer):
    content = serializers.CharField(required=True, min_length=1, max_length=500)

class UpdateCommentRequestSerializer(serializers.Serializer):
    content = serializers.CharField(required=True, min_length=1, max_length=500)

class CommentListResponseSerializer(serializers.Serializer):
    comments = CommentResponseSerializer(many=True, read_only=True)
    total_count = serializers.IntegerField(read_only=True)
    page = serializers.IntegerField(read_only=True)
    page_size = serializers.IntegerField(read_only=True)
    total_pages = serializers.IntegerField(read_only=True)

class PaginationInfoRequestSerializer(serializers.Serializer):
    page_number = serializers.IntegerField(default=1, min_value=1)
    page_size = serializers.IntegerField(default=10, min_value=1, max_value=50)