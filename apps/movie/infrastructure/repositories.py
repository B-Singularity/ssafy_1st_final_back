# 파일 경로: apps/movie/infrastructure/repositories.py
# from typing import Optional, List # 타입 힌트 제거
from django.db import transaction
from django.db.models import Q, Avg, Subquery, OuterRef, FloatField, Value
from django.db.models.functions import Coalesce

from apps.movie.domain.aggregates.movie import Movie
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

from apps.movie.domain.repositories import MovieRepository, MovieSearchRepository
from apps.movie.models import MovieModel, GenreModel, PersonModel, MovieCastMemberModel, StillCutModel, TrailerModel, MoviePlatformRatingModel, OTTPlatformModel, MovieOTTAvailabilityModel
from apps.movie.application.dtos import MovieSearchCriteriaDto, MovieSearchResultDto, SearchedMovieItemDto, PaginationDto, FilterOptionsDto, SortOptionDto
import datetime


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
                cast_vo.append(ActorVO(name=cast_member.actor.name, role_name=cast_member.role_name, external_id=cast_member.actor.external_id))

        still_cuts_vo = [StillCutVO(image_url=sc.image_url, caption=sc.caption, display_order=sc.display_order) for sc in movie_model.still_cuts.all()]
        trailers_vo = [TrailerVO(url=t.url, trailer_type=t.trailer_type, site_name=t.site_name, thumbnail_url=t.thumbnail_url) for t in movie_model.trailers.all()]
        
        platform_ratings_vo = []
        if hasattr(movie_model, 'platform_ratings'):
            for r in movie_model.platform_ratings.all():
                 platform_ratings_vo.append(MoviePlatformRatingVO(platform_name=r.platform_name, score=r.score))

        ott_availability_vo = []
        if hasattr(movie_model, 'ott_availability'):
            for o in movie_model.ott_availability.select_related('platform').all():
                ott_availability_vo.append(OTTInfoVO(platform_name=o.platform.name, watch_url=o.watch_url, logo_image_url=o.platform.logo_image_url, availability_note=o.availability_note))
        
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
            return self._to_domain_object(movie_model)
        except MovieModel.DoesNotExist:
            return None

    @transaction.atomic
    def save(self, movie):  # 타입 힌트는 이전 요청에 따라 제거
        defaults_to_set = {
            'korean_title': movie.title_info.korean_title,
            'original_title': movie.title_info.original_title,
            'plot': movie.plot.text if movie.plot else None,
            'release_date': movie.release_date.release_date if movie.release_date else None,
            'runtime_minutes': movie.runtime.minutes if movie.runtime else None,
            'poster_image_url': movie.poster_image.url if movie.poster_image else None,
            'updated_at': movie.updated_at if movie.updated_at else datetime.now(),
        }

        if movie.movie_id and movie.movie_id > 0:
            # ID가 존재하면 업데이트 시나리오
            # created_at은 업데이트하지 않으므로 defaults_to_set에 포함하지 않음
            movie_model, created = MovieModel.objects.update_or_create(
                id=movie.movie_id,
                defaults=defaults_to_set
            )
            if created:
                # ID가 있었지만 DB에 없어 새로 생성된 경우 (일반적이지 않은 AutoField 시나리오)
                # 이 경우 created_at을 도메인 객체의 값으로 설정할 수 있음
                if movie.created_at:
                    movie_model.created_at = movie.created_at
                    movie_model.save(update_fields=['created_at'])
        else:
            # ID가 없거나 0이면 신규 생성 시나리오
            # MovieModel의 created_at 필드에 auto_now_add=True가 있다면,
            # create 시 자동으로 설정되므로 defaults_to_set에 추가할 필요 없음.
            # 만약 도메인 객체의 created_at 값을 우선적으로 사용하고 싶다면,
            # 모델 필드의 auto_now_add를 False로 하거나 default=timezone.now 등으로 하고 여기서 설정.
            if movie.created_at:
                defaults_to_set['created_at'] = movie.created_at

            # MovieModel의 id가 AutoField이므로, id 없이 create
            movie_model = MovieModel.objects.create(**defaults_to_set)
            # created = True # 이 변수는 이후 로직에서 사용되지 않는다면 불필요

        # 관계 필드 처리
        genre_instances = []
        for genre_vo in movie.genres:
            genre_instance, _ = GenreModel.objects.get_or_create(name=genre_vo.name)
            genre_instances.append(genre_instance)
        movie_model.genres.set(genre_instances)

        director_instances = []
        for director_vo in movie.directors:
            person_instance, _ = PersonModel.objects.get_or_create(name=director_vo.name,
                                                                   defaults={'external_id': director_vo.external_id})
            director_instances.append(person_instance)
        movie_model.directors.set(director_instances)

        MovieCastMemberModel.objects.filter(movie=movie_model).delete()
        for actor_vo in movie.cast:
            actor_instance, _ = PersonModel.objects.get_or_create(name=actor_vo.name,
                                                                  defaults={'external_id': actor_vo.external_id})
            MovieCastMemberModel.objects.create(movie=movie_model, actor=actor_instance, role_name=actor_vo.role_name)

        MoviePlatformRatingModel.objects.filter(movie=movie_model).delete()
        for rating_vo in movie.platform_ratings:
            MoviePlatformRatingModel.objects.create(movie=movie_model, platform_name=rating_vo.platform_name,
                                                    score=rating_vo.score)

        MovieOTTAvailabilityModel.objects.filter(movie=movie_model).delete()
        for ott_vo in movie.ott_availability:
            platform_instance, _ = OTTPlatformModel.objects.get_or_create(name=ott_vo.platform_name, defaults={
                'logo_image_url': ott_vo.logo_image_url})
            MovieOTTAvailabilityModel.objects.create(movie=movie_model, platform=platform_instance,
                                                     watch_url=ott_vo.watch_url,
                                                     availability_note=ott_vo.availability_note)

        # 저장 또는 생성된 movie_model을 기반으로 도메인 객체를 다시 만듭니다.
        # 이렇게 하면 DB에 의해 자동 생성/수정된 값(예: id, auto_now_add, auto_now 필드)이 반영됩니다.
        return self._to_domain_object(movie_model)

    @transaction.atomic
    def delete(self, movie_id):
        MovieModel.objects.filter(id=movie_id).delete()


class DjangoMovieSearchRepository(MovieSearchRepository):
    def search_movies(self, criteria):
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

        sort_direction = ""
        if criteria.sort_by:
            sort_direction = "-" if criteria.sort_by.direction.lower() == "desc" else ""
            sort_field = criteria.sort_by.field
            rating_platform_to_sort_by = criteria.sort_by.rating_platform

            if sort_field == "rating":
                if rating_platform_to_sort_by:
                    platform_score_subquery = MoviePlatformRatingModel.objects.filter(
                        movie=OuterRef('pk'),
                        platform_name=rating_platform_to_sort_by 
                    ).values('score')[:1]
                    
                    queryset = queryset.annotate(
                        relevant_score=Coalesce(Subquery(platform_score_subquery, output_field=FloatField()), Value(0.0))
                    ).order_by(f'{sort_direction}relevant_score', '-created_at')
                else:
                    queryset = queryset.annotate(
                        default_rating_score=Avg('platform_ratings__score') # 예시: 모든 플랫폼 평균 또는 특정 기본 플랫폼
                    ).order_by(f'{sort_direction}default_rating_score', '-created_at')
            elif sort_field == "release_date":
                queryset = queryset.order_by(f'{sort_direction}release_date', '-created_at')
            else: 
                queryset = queryset.order_by(f'{sort_direction}korean_title', '-created_at')
        else:
            queryset = queryset.order_by('-release_date', '-created_at')

        total_results = queryset.count()
        
        start = (criteria.pagination.page_number - 1) * criteria.pagination.page_size
        end = start + criteria.pagination.page_size
        movies_page_qs = queryset[start:end]

        searched_movies_dto_list = []
        for movie_model in movies_page_qs:
            rating_val = None
            display_platform = "TMDB" # 기본 표시 평점 플랫폼
            if criteria.sort_by and criteria.sort_by.field == "rating" and criteria.sort_by.rating_platform:
                display_platform = criteria.sort_by.rating_platform
            
            if hasattr(movie_model, 'relevant_score') and display_platform == (criteria.sort_by.rating_platform if criteria.sort_by else None):
                 rating_val = round(movie_model.relevant_score, 1) if movie_model.relevant_score is not None else None
            elif hasattr(movie_model, 'default_rating_score') and not (criteria.sort_by and criteria.sort_by.rating_platform):
                 rating_val = round(movie_model.default_rating_score, 1) if movie_model.default_rating_score is not None else None
            else:
                rating_qs = movie_model.platform_ratings.filter(platform_name=display_platform).first()
                rating_val = round(rating_qs.score, 1) if rating_qs else None

            searched_movies_dto_list.append(SearchedMovieItemDto(
                movie_id=movie_model.id,
                title=movie_model.korean_title,
                poster_image_url=movie_model.poster_image_url,
                release_year=movie_model.release_date.year if movie_model.release_date else None,
                rating=rating_val
            ))
        
        total_pages = (total_results + criteria.pagination.page_size - 1) // criteria.pagination.page_size
        message = "검색 결과가 없습니다." if total_results == 0 else None

        return MovieSearchResultDto(
            movies=searched_movies_dto_list,
            total_results=total_results,
            current_page=criteria.pagination.page_number,
            total_pages=total_pages,
            message=message
        )

    def find_popular_movies(self, 
                              list_type_criterion,
                              genre_filter,
                              pagination
                             ):
        
        queryset = MovieModel.objects.all()

        if genre_filter:
            queryset = queryset.filter(genres__name=genre_filter)

        order_by_fields = []
        rating_platform_for_popular = None # 인기 영화 DTO에 표시할 평점 플랫폼

        if list_type_criterion == "top_rated_tmdb":
            rating_platform_for_popular = "TMDB"
            platform_score_subquery = MoviePlatformRatingModel.objects.filter(
                movie=OuterRef('pk'), platform_name=rating_platform_for_popular
            ).values('score')[:1]
            queryset = queryset.annotate(relevant_score=Coalesce(Subquery(platform_score_subquery, output_field=FloatField()), Value(0.0)))
            order_by_fields.extend(['-relevant_score', '-created_at'])
        elif list_type_criterion == "top_rated_watcha":
            rating_platform_for_popular = "왓차"
            platform_score_subquery = MoviePlatformRatingModel.objects.filter(
                movie=OuterRef('pk'), platform_name=rating_platform_for_popular
            ).values('score')[:1]
            queryset = queryset.annotate(relevant_score=Coalesce(Subquery(platform_score_subquery, output_field=FloatField()), Value(0.0)))
            order_by_fields.extend(['-relevant_score', '-created_at'])
        elif list_type_criterion == "latest_highly_rated":
            rating_platform_for_popular = "TMDB" 
            platform_score_subquery = MoviePlatformRatingModel.objects.filter(
                movie=OuterRef('pk'), platform_name=rating_platform_for_popular
            ).values('score')[:1]
            queryset = queryset.annotate(relevant_score_for_latest=Coalesce(Subquery(platform_score_subquery, output_field=FloatField()), Value(0.0)))
            order_by_fields.extend(['-release_date', '-relevant_score_for_latest', '-created_at'])
        else: 
            rating_platform_for_popular = "TMDB" # 기본 인기 영화도 TMDB 평점 사용
            order_by_fields.extend(['-created_at']) # 예시: 기본은 등록순 (또는 다른 인기 지표)
        
        queryset = queryset.order_by(*order_by_fields).distinct()

        total_results = queryset.count()
        
        start = (pagination.page_number - 1) * pagination.page_size
        end = start + pagination.page_size
        movies_page_qs = queryset[start:end]

        searched_movies_dto_list = []
        for movie_model in movies_page_qs:
            rating_val = None
            if hasattr(movie_model, 'relevant_score'): # top_rated_tmdb, top_rated_watcha
                rating_val = round(movie_model.relevant_score, 1) if movie_model.relevant_score is not None else None
            elif hasattr(movie_model, 'relevant_score_for_latest'): # latest_highly_rated
                rating_val = round(movie_model.relevant_score_for_latest, 1) if movie_model.relevant_score_for_latest is not None else None
            elif rating_platform_for_popular: # 기본 fallback
                rating_qs = movie_model.platform_ratings.filter(platform_name=rating_platform_for_popular).first()
                rating_val = round(rating_qs.score, 1) if rating_qs else None
            
            searched_movies_dto_list.append(SearchedMovieItemDto(
                movie_id=movie_model.id,
                title=movie_model.korean_title,
                poster_image_url=movie_model.poster_image_url,
                release_year=movie_model.release_date.year if movie_model.release_date else None,
                rating=rating_val
            ))
        
        total_pages = (total_results + pagination.page_size - 1) // pagination.page_size
        message = "인기 영화 목록 결과가 없습니다." if total_results == 0 else None

        return MovieSearchResultDto(
            movies=searched_movies_dto_list,
            total_results=total_results,
            current_page=pagination.page_number,
            total_pages=total_pages,
            message=message
        )