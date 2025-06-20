import logging

from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
from django.db.models import Q, Avg, Subquery, OuterRef, FloatField, Value
from django.db.models.functions import Coalesce
import datetime

from src.apps.movie.domain.aggregates.movie import Movie

from src.apps.movie.application.ports.repositories import MovieRepository, MovieSearchRepository
from src.apps.movie.application.dtos import MovieSearchResultDto, SearchedMovieItemDto
from src.apps.movie.domain.value_objects.actor_vo import ActorVO
from src.apps.movie.domain.value_objects.director_vo import DirectorVO
from src.apps.movie.domain.value_objects.genre_vo import GenreVO
from src.apps.movie.domain.value_objects.movie_platform_rating_vo import MoviePlatformRatingVO
from src.apps.movie.domain.value_objects.ott_info_vo import OTTInfoVO
from src.apps.movie.domain.value_objects.plot_vo import PlotVO
from src.apps.movie.domain.value_objects.poster_image_vo import PosterImageVO
from src.apps.movie.domain.value_objects.release_date_vo import ReleaseDateVO
from src.apps.movie.domain.value_objects.runtime_vo import RuntimeVO
from src.apps.movie.domain.value_objects.still_cut_vo import StillCutVO
from src.apps.movie.domain.value_objects.title_info_vo import TitleInfoVO
from src.apps.movie.domain.value_objects.trailer_vo import TrailerVO
from src.apps.movie.models import MovieModel, GenreModel, PersonModel, MovieCastMemberModel, MoviePlatformRatingModel

logger = logging.getLogger(__name__)


class DjangoMovieRepository(MovieRepository):
    def _to_domain_object(self, movie_model):
        if not movie_model:
            return None

        title_info_vo = TitleInfoVO(korean_title=movie_model.korean_title, original_title=movie_model.original_title)
        plot_vo = PlotVO(text=movie_model.plot)
        release_date_vo = ReleaseDateVO(release_date=movie_model.release_date) if movie_model.release_date else None
        runtime_vo = RuntimeVO(minutes=movie_model.runtime_minutes) if movie_model.runtime_minutes is not None else None
        poster_image_vo = PosterImageVO(url=movie_model.poster_image_url) if movie_model.poster_image_url else None

        genres_vo = [GenreVO(name=g.name) for g in movie_model.genres.all()]
        directors_vo = [DirectorVO(name=d.name, external_id=d.external_id) for d in movie_model.directors.all()]

        cast_vo = []
        if hasattr(movie_model, 'cast_members'):
            for cast_member in movie_model.cast_members.select_related('actor').all():
                cast_vo.append(ActorVO(name=cast_member.actor.name, role_name=cast_member.role_name,
                                       external_id=cast_member.actor.external_id))

        still_cuts_vo = [StillCutVO(image_url=sc.image_url, caption=sc.caption, display_order=sc.display_order) for sc
                         in movie_model.still_cuts.all()]
        trailers_vo = [
            TrailerVO(url=t.url, trailer_type=t.trailer_type, site_name=t.site_name, thumbnail_url=t.thumbnail_url) for
            t in movie_model.trailers.all()]

        platform_ratings_vo = []
        if hasattr(movie_model, 'platform_ratings'):
            for r in movie_model.platform_ratings.all():
                platform_ratings_vo.append(MoviePlatformRatingVO(platform_name=r.platform_name, score=r.score))

        ott_availability_vo = []
        if hasattr(movie_model, 'ott_availability'):
            for o in movie_model.ott_availability.select_related('platform').all():
                ott_availability_vo.append(OTTInfoVO(platform_name=o.platform.name, watch_url=o.watch_url,
                                                     logo_image_url=o.platform.logo_image_url,
                                                     availability_note=o.availability_note))

        return Movie(
            movie_id=movie_model.id,
            title_info=title_info_vo,
            plot=plot_vo,
            release_date=release_date_vo,
            runtime=runtime_vo,
            poster_image=poster_image_vo,
            genres=genres_vo,
            directors=directors_vo,
            cast=cast_vo,
            still_cuts=still_cuts_vo,
            trailers=trailers_vo,
            platform_ratings=platform_ratings_vo,
            ott_availability=ott_availability_vo,
            created_at=movie_model.created_at,
            updated_at=movie_model.updated_at
        )

    def find_by_id(self, movie_id):
        try:
            movie_model = MovieModel.objects.prefetch_related(
                'genres', 'directors', 'cast_members__actor',
                'still_cuts', 'trailers', 'platform_ratings',
                'ott_availability__platform'
            ).get(id=movie_id)
            logger.info(f"DB에 MovieModel찾음: {movie_id}")
            return self._to_domain_object(movie_model)
        except ObjectDoesNotExist:
            logger.warning(f"MovieModel not found in DB for id: {movie_id}")
            return None

    @transaction.atomic
    def save(self, movie: Movie):
        logger.info(f"데이터 베이스에 영화 저장 중, Movie ID: {movie.movie_id}, Title: {movie.title_info.korean_title}")
        defaults = {
            'korean_title': movie.title_info.korean_title,
            'original_title': movie.title_info.original_title,
            'plot': movie.plot.text if movie.plot else None,
            'release_date': movie.release_date.release_date if movie.release_date else None,
            'runtime_minutes': movie.runtime.minutes if movie.runtime else None,
            'poster_image_url': movie.poster_image.url if movie.poster_image else None,
            'updated_at': movie.updated_at if movie.updated_at else datetime.datetime.now(),
        }

        if movie.movie_id and movie.movie_id > 0:
            movie_model, created = MovieModel.objects.update_or_create(id=movie.movie_id, defaults=defaults)
        else:
            if movie.created_at:
                defaults['created_at'] = movie.created_at
            movie_model = MovieModel.objects.create(**defaults)
            created = True

        logger.info(f"영화가 저장되었습니다. ID: {movie_model.id}, Created: {created}")

        genre_instances = [GenreModel.objects.get_or_create(name=g.name)[0] for g in movie.genres]
        movie_model.genres.set(genre_instances)

        director_instances = [PersonModel.objects.get_or_create(name=d.name, defaults={'external_id': d.external_id})[0] for d in movie.directors]
        movie_model.directors.set(director_instances)

        MovieCastMemberModel.objects.filter(movie_id=movie_model.id).delete()
        for actor_vo in movie.cast:
            actor_instance = PersonModel.objects.get_or_create(name=actor_vo.name, defaults={'external_id': actor_vo.external_id})[0]
            MovieCastMemberModel.objects.create(movie_id=movie_model.id, actor=actor_instance)

        return self._to_domain_object(MovieModel.objects.get(id=movie_model.id))

    @transaction.atomic
    def delete(self, movie_id):
        logger.warning(f"데이터베이스에서 영화를 삭제합니다. Movie ID: {movie_id}")
        deleted_count, _ = MovieModel.objects.filter(id=movie_id).delete()
        if deleted_count > 0:
            logger.info(f"성공적으로 영화가 삭제되었습니다. Movie ID: {movie_id}")
        else:
            logger.warning(f"존재하지 않는 영화를 삭제 시도했습니다.")


class DjangoMovieSearchRepository(MovieSearchRepository):
    def search_movies(self, criteria):
        logger.info(f"Executing movie search in database with criteria: {criteria.__dict__}")
        queryset = MovieModel.objects.all()

        if criteria.keyword:
            queryset = queryset.filter(
                Q(korean_title__icontains=criteria.keyword) |
                Q(original_title__icontains=criteria.keyword) |
                Q(directors__name__icontains=criteria.keyword) |
                Q(cast_members__actor__name__icontains=criteria.keyword)
            ).distinct()

        if criteria.filters:
            if criteria.filters.genres:
                queryset = queryset.filter(genres__name__in=criteria.filters.genres).distinct()
            if criteria.filters.release_year_from:
                queryset = queryset.filter(release_date__year__gte=criteria.filters.release_year_from)
            if criteria.filters.release_year_to:
                queryset = queryset.filter(release_date__year__lte=criteria.filters.release_year_to)

        if criteria.sort_by:
            sort_direction = "-" if criteria.sort_by.direction == "desc" else ""
            sort_field = criteria.sort_by.field

            if sort_field == "rating" and criteria.sort_by.rating_platform:
                platform_score = Subquery(
                    MoviePlatformRatingModel.objects.filter(
                        movie=OuterRef('pk'),
                        platform_name=criteria.sort_by.rating_platform
                    ).values('score')[:1]
                )
                queryset = queryset.annotate(
                    relevant_score=Coalesce(platform_score, Value(0.0), output_field=FloatField())
                ).order_by(f'{sort_direction}relevant_score', '-created_at')
            elif sort_field == "release_date":
                queryset = queryset.order_by(f'{sort_direction}release_date', '-created_at')
            else:
                queryset = queryset.order_by(f'{sort_direction}korean_title', '-created_at')
        else:
            queryset = queryset.order_by('-created_at')

        total_results = queryset.count()
        start = (criteria.pagination.page_number - 1) * criteria.pagination.page_size
        end = start + criteria.pagination.page_size
        paginated_qs = queryset[start:end]

        movies_dto_list = [
            SearchedMovieItemDto(
                movie_id=movie.id,
                title=movie.korean_title,
                poster_image_url=movie.poster_image_url,
                release_year=movie.release_date.year if movie.release_date else None,
                rating=round(getattr(movie, 'relevant_score', 0.0), 1)
            ) for movie in paginated_qs
        ]

        total_pages = (total_results + criteria.pagination.page_size - 1) // criteria.pagination.page_size
        return MovieSearchResultDto(
            movies=movies_dto_list,
            total_results=total_results,
            current_page=criteria.pagination.page_number,
            total_pages=total_pages
        )

    def find_popular_movies(self, list_type_criterion, genre_filter, pagination):
        logger.info(f"Executing popular movie search in database. Type: {list_type_criterion}")
        queryset = MovieModel.objects.all().order_by('-release_date', '-created_at')
        if genre_filter:
            queryset = queryset.filter(genres__name=genre_filter)

        total_results = queryset.count()
        start = (pagination.page_number - 1) * pagination.page_size
        end = start + pagination.page_size
        paginated_qs = queryset[start:end]

        movies_dto_list = [
            SearchedMovieItemDto(
                movie_id=movie.id,
                title=movie.korean_title,
                poster_image_url=movie.poster_image_url,
                release_year=movie.release_date.year if movie.release_date else None,
                rating=None
            ) for movie in paginated_qs
        ]

        total_pages = (total_results + pagination.page_size - 1) // pagination.page_size
        return MovieSearchResultDto(
            movies=movies_dto_list,
            total_results=total_results,
            current_page=pagination.page_number,
            total_pages=total_pages
        )