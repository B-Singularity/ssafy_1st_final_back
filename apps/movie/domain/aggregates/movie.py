from datetime import date, datetime

from apps.movie.domain.value_objects.title_info_vo import TitleInfoVO
from apps.movie.domain.value_objects.plot_vo import PlotVO
from apps.movie.domain.value_objects.release_date_vo import ReleaseDateVO
from apps.movie.domain.value_objects.runtime_vo import RuntimeVO
from apps.movie.domain.value_objects.poster_image_vo import PosterImageVO
from apps.movie.domain.value_objects.genre_vo import GenreVO
from apps.movie.domain.value_objects.director_vo import DirectorVO
from apps.movie.domain.value_objects.actor_vo import ActorVO
from apps.movie.domain.value_objects.still_cut_vo import StillCutVO
from apps.movie.domain.value_objects.trailer_vo import TrailerVO
from apps.movie.domain.value_objects.movie_platform_rating_vo import MoviePlatformRatingVO
from apps.movie.domain.value_objects.ott_info_vo import OTTInfoVO

class Movie:
    def __init__(self,
                 movie_id,
                 title_info,
                 plot,
                 release_date, 
                 runtime,
                 poster_image,
                 genres, # 항상 리스트를 기대 (빈 리스트 가능)
                 directors, # 항상 리스트를 기대 (빈 리스트 가능)
                 cast,      # 항상 리스트를 기대 (빈 리스트 가능)
                 still_cuts, # 항상 리스트를 기대 (빈 리스트 가능)
                 trailers,   # 항상 리스트를 기대 (빈 리스트 가능)
                 platform_ratings, # 항상 리스트를 기대 (빈 리스트 가능)
                 ott_availability, # 항상 리스트를 기대 (빈 리스트 가능)
                 created_at=None,
                 updated_at=None):

        if not isinstance(movie_id, int) or movie_id <= 0:
            raise ValueError("영화 ID는 0보다 큰 정수여야 합니다.")
        if not isinstance(title_info, TitleInfoVO):
            raise TypeError("title_info는 TitleInfoVO의 인스턴스여야 합니다.")
        if not isinstance(plot, PlotVO):
            raise TypeError("plot은 PlotVO의 인스턴스여야 합니다.")
        
        if release_date is not None and not isinstance(release_date, ReleaseDateVO):
            raise TypeError("release_date가 None이 아니면 ReleaseDateVO의 인스턴스여야 합니다.")
            
        if runtime is not None and not isinstance(runtime, RuntimeVO):
            raise TypeError("runtime이 None이 아니면 RuntimeVO의 인스턴스여야 합니다.")

        if poster_image is not None and not isinstance(poster_image, PosterImageVO):
            raise TypeError("poster_image가 None이 아니면 PosterImageVO의 인스턴스여야 합니다.")
        
        if not isinstance(genres, list) or not all(isinstance(g, GenreVO) for g in genres):
            raise TypeError("genres는 GenreVO 객체의 리스트여야 합니다.")
        if not isinstance(directors, list) or not all(isinstance(d, DirectorVO) for d in directors):
            raise TypeError("directors는 DirectorVO 객체의 리스트여야 합니다.")
        if not isinstance(cast, list) or not all(isinstance(a, ActorVO) for a in cast):
            raise TypeError("cast는 ActorVO 객체의 리스트여야 합니다.")
        
        if not isinstance(still_cuts, list) or not all(isinstance(sc, StillCutVO) for sc in still_cuts):
            raise TypeError("still_cuts는 StillCutVO 객체의 리스트여야 합니다.")
        if not isinstance(trailers, list) or not all(isinstance(t, TrailerVO) for t in trailers):
            raise TypeError("trailers는 TrailerVO 객체의 리스트여야 합니다.")
        if not isinstance(platform_ratings, list) or not all(isinstance(pr, MoviePlatformRatingVO) for pr in platform_ratings):
            raise TypeError("platform_ratings는 MoviePlatformRatingVO 객체의 리스트여야 합니다.")
        if not isinstance(ott_availability, list) or not all(isinstance(oa, OTTInfoVO) for oa in ott_availability):
            raise TypeError("ott_availability는 OTTInfoVO 객체의 리스트여야 합니다.")
        
        if created_at is not None and not isinstance(created_at, datetime):
            raise TypeError("created_at이 None이 아니면 datetime 객체여야 합니다.")
        if updated_at is not None and not isinstance(updated_at, datetime):
            raise TypeError("updated_at이 None이 아니면 datetime 객체여야 합니다.")

        self._movie_id = movie_id
        self._title_info = title_info
        self._plot = plot
        self._release_date = release_date
        self._runtime = runtime
        self._poster_image = poster_image
        self._genres = list(genres) 
        self._directors = list(directors) 
        self._cast = list(cast) 
        
        self._still_cuts = list(still_cuts) 
        self._trailers = list(trailers) 
        self._platform_ratings = list(platform_ratings) 
        self._ott_availability = list(ott_availability) 
        
        current_time = datetime.now() 
        self._created_at = created_at if created_at else current_time
        self._updated_at = updated_at if updated_at else current_time

    # ... (프로퍼티 및 다른 메서드는 이전과 동일하게 유지) ...
    @property
    def movie_id(self):
        return self._movie_id

    @property
    def title_info(self):
        return self._title_info

    @property
    def plot(self):
        return self._plot

    @property
    def release_date(self):
        return self._release_date

    @property
    def runtime(self):
        return self._runtime

    @property
    def poster_image(self):
        return self._poster_image

    @property
    def genres(self):
        return list(self._genres)

    @property
    def directors(self):
        return list(self._directors)

    @property
    def cast(self):
        return list(self._cast)

    @property
    def still_cuts(self):
        return list(self._still_cuts)

    @property
    def trailers(self):
        return list(self._trailers)

    @property
    def platform_ratings(self):
        return list(self._platform_ratings)

    @property
    def ott_availability(self):
        return list(self._ott_availability)
        
    @property
    def created_at(self):
        return self._created_at
        
    @property
    def updated_at(self):
        return self._updated_at

    def __eq__(self, other):
        if not isinstance(other, Movie):
            return NotImplemented
        return self._movie_id == other._movie_id

    def __hash__(self):
        return hash(self._movie_id)

    def __str__(self):
        if self._title_info and hasattr(self._title_info, 'korean_title'):
            return str(self._title_info.korean_title)
        return f"Movie (ID: {self._movie_id})"

    def update_plot(self, new_plot):
        if not isinstance(new_plot, PlotVO):
            raise TypeError("새로운 줄거리는 PlotVO의 인스턴스여야 합니다.")
        self._plot = new_plot
        self._updated_at = datetime.now()

    def add_genre(self, genre):
        if not isinstance(genre, GenreVO):
            raise TypeError("추가할 장르는 GenreVO의 인스턴스여야 합니다.")
        if genre not in self._genres:
            self._genres.append(genre)
            self._updated_at = datetime.now()

    def remove_genre(self, genre_to_remove):
        if not isinstance(genre_to_remove, GenreVO):
            raise TypeError("삭제할 장르는 GenreVO의 인스턴스여야 합니다.")
        if genre_to_remove in self._genres:
            self._genres.remove(genre_to_remove)
            self._updated_at = datetime.now()
