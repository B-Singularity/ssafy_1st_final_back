import logging
from django.contrib import admin

from src.apps.movie.models import MovieCastMemberModel, StillCutModel, TrailerModel, MoviePlatformRatingModel, \
    MovieOTTAvailabilityModel, MovieModel, PersonModel, GenreModel, OTTPlatformModel

logger = logging.getLogger(__name__)


# 인라인(Inline) 정의
class MovieCastMemberInline(admin.TabularInline):
    model = MovieCastMemberModel
    extra = 1
    autocomplete_fields = ['actor']


class StillCutInline(admin.TabularInline):
    model = StillCutModel
    extra = 1


class TrailerInline(admin.TabularInline):
    model = TrailerModel
    extra = 1


class MoviePlatformRatingInline(admin.TabularInline):
    model = MoviePlatformRatingModel
    extra = 1


class MovieOTTAvailabilityInline(admin.TabularInline):
    model = MovieOTTAvailabilityModel
    extra = 1
    autocomplete_fields = ['platform']


@admin.register(MovieModel)
class MovieAdmin(admin.ModelAdmin):
    list_display = ('korean_title', 'release_date', 'runtime_minutes', 'created_at')
    list_filter = ('release_date', 'genres')
    search_fields = ('korean_title', 'original_title', 'directors__name')
    filter_horizontal = ('genres', 'directors')
    inlines = [
        MovieCastMemberInline,
        MoviePlatformRatingInline,
        MovieOTTAvailabilityInline,
        StillCutInline,
        TrailerInline,
    ]

    def save_model(self, request, obj, form, change):
        logger.info(f"Movie '{obj.korean_title}' is being saved by admin user '{request.user}'. Change: {change}")
        super().save_model(request, obj, form, change)


@admin.register(PersonModel)
class PersonAdmin(admin.ModelAdmin):
    list_display = ('name', 'external_id')
    search_fields = ('name',)


@admin.register(GenreModel)
class GenreAdmin(admin.ModelAdmin):
    search_fields = ('name',)


@admin.register(OTTPlatformModel)
class OTTPlatformAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


admin.site.register(MovieCastMemberModel)
admin.site.register(StillCutModel)
admin.site.register(TrailerModel)
admin.site.register(MoviePlatformRatingModel)
admin.site.register(MovieOTTAvailabilityModel)