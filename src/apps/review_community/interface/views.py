from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny 

from .serializers import (
    CreateCommentRequestSerializer, UpdateCommentRequestSerializer,
    CommentResponseSerializer, CommentListResponseSerializer,
    PaginationInfoRequestSerializer
)
from ..application.dtos import (
    CreateCommentRequestDto, UpdateCommentRequestDto, PaginationInfoRequestDto
)
from ..application.services import CommentAppService
from ..infrastructure.repositories import DjangoCommentThreadRepository


def get_comment_app_service():
    comment_thread_repo = DjangoCommentThreadRepository()
    return CommentAppService(comment_thread_repository=comment_thread_repo)


class MovieCommentListCreateAPIView(APIView):
    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAuthenticated()]
        return [AllowAny()]

    def get(self, request, movie_id):
        pagination_serializer = PaginationInfoRequestSerializer(data=request.query_params)
        if not pagination_serializer.is_valid():
            return Response(pagination_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        pagination_dto = PaginationInfoRequestDto(**pagination_serializer.validated_data)
        service = get_comment_app_service()
        
        try:
            comment_list_dto = service.get_comments_for_movie(movie_id, pagination_dto)
            response_serializer = CommentListResponseSerializer(comment_list_dto)
            return Response(response_serializer.data)
        except Exception as e:
            return Response({"error": "댓글 목록 조회 중 오류 발생"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request, movie_id):
        serializer = CreateCommentRequestSerializer(data=request.data)
        if serializer.is_valid():
            request_dto = CreateCommentRequestDto(
                movie_id=movie_id,
                content=serializer.validated_data['content']
            )
            service = get_comment_app_service()
            try:
                author_user_instance = request.user
                
                comment_dto = service.add_comment_to_movie(author_user_instance, request_dto)
                response_serializer = CommentResponseSerializer(comment_dto)
                return Response(response_serializer.data, status=status.HTTP_201_CREATED)
            except ValueError as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
            except Exception as e:
                return Response({"error": "댓글 작성 중 오류 발생"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MovieCommentDetailAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, movie_id, comment_id_str):
        serializer = UpdateCommentRequestSerializer(data=request.data)
        if serializer.is_valid():
            request_dto = UpdateCommentRequestDto(content=serializer.validated_data['content'])
            service = get_comment_app_service()
            author_account_id = request.user.id

            try:
                updated_comment_dto = service.update_comment(movie_id, comment_id_str, author_account_id, request_dto)
                if updated_comment_dto:
                    response_serializer = CommentResponseSerializer(updated_comment_dto)
                    return Response(response_serializer.data)
                return Response({"error": "댓글을 찾을 수 없거나 수정 권한이 없습니다."}, status=status.HTTP_404_NOT_FOUND)
            except ValueError as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
            except PermissionError as e:
                return Response({"error": str(e)}, status=status.HTTP_403_FORBIDDEN)
            except Exception as e:
                return Response({"error": "댓글 수정 중 오류 발생"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, movie_id, comment_id_str):
        service = get_comment_app_service()
        author_account_id = request.user.id
        try:
            service.delete_comment(movie_id, comment_id_str, author_account_id)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except PermissionError as e:
            return Response({"error": str(e)}, status=status.HTTP_403_FORBIDDEN)
        except ValueError as e: 
             return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": "댓글 삭제 중 오류 발생"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)