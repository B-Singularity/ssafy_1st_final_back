from django.urls import path
from .views import MovieCommentListCreateAPIView, MovieCommentDetailAPIView

urlpatterns = [
    path('<int:movie_id>/comments/', MovieCommentListCreateAPIView.as_view(), name='movie_comment_list_create'),
    path('<int:movie_id>/comments/<uuid:comment_id_str>/', MovieCommentDetailAPIView.as_view(), name='movie_comment_detail'),
]