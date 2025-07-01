from django.urls import path
from .views import MovieSearchAPIView, MovieDetailAPIView, PopularMoviesAPIView

urlpatterns = [
    path('search', MovieSearchAPIView.as_view(), name='movie_search'),
    path('<int:movie_id>', MovieDetailAPIView.as_view(), name='movie_detail'),
    path('popular', PopularMoviesAPIView.as_view(), name='popular_movies'),
]