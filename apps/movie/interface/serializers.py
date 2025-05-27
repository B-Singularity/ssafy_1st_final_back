from rest_framework import serializers


class MovieSearchQueryParamSerializer(serializers.Serializer):
    keyword = serializers.CharField(required=False, allow_blank=True, max_length=100, allow_null=True)
    genres = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    release_year_from = serializers.IntegerField(required=False, allow_null=True)
    release_year_to = serializers.IntegerField(required=False, allow_null=True)
    sort_field = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    sort_direction = serializers.ChoiceField(choices=['asc', 'desc'], required=False, allow_blank=True, allow_null=True)
    rating_platform = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    page_number = serializers.IntegerField(required=False, min_value=1, allow_null=True)
    page_size = serializers.IntegerField(required=False, min_value=1, max_value=100, allow_null=True)


class SearchedMovieItemResponseSerializer(serializers.Serializer):
    movie_id = serializers.IntegerField()
    title = serializers.CharField()
    poster_image_url = serializers.URLField(allow_null=True)
    release_year = serializers.IntegerField(allow_null=True)
    rating = serializers.FloatField(allow_null=True)

class MovieSearchResultResponseSerializer(serializers.Serializer):
    movies = SearchedMovieItemResponseSerializer(many=True)
    total_results = serializers.IntegerField()
    current_page = serializers.IntegerField()
    total_pages = serializers.IntegerField()
    message = serializers.CharField(allow_null=True, required=False)

class TitleInfoDisplayResponseSerializer(serializers.Serializer):
    korean_title = serializers.CharField()
    original_title = serializers.CharField(allow_null=True, required=False)

class PlotDisplayResponseSerializer(serializers.Serializer):
    text = serializers.CharField(allow_null=True, required=False)
        
class StillCutDisplayResponseSerializer(serializers.Serializer):
    image_url = serializers.URLField()
    caption = serializers.CharField(allow_null=True, required=False)
    display_order = serializers.IntegerField()

class TrailerDisplayResponseSerializer(serializers.Serializer):
    url = serializers.URLField()
    trailer_type = serializers.CharField(allow_null=True, required=False)
    site_name = serializers.CharField(allow_null=True, required=False)
    thumbnail_url = serializers.URLField(allow_null=True, required=False)

class MoviePlatformRatingDisplayResponseSerializer(serializers.Serializer):
    platform_name = serializers.CharField()
    score = serializers.FloatField()

class OTTInfoDisplayResponseSerializer(serializers.Serializer):
    platform_name = serializers.CharField()
    watch_url = serializers.URLField(allow_null=True, required=False)
    logo_image_url = serializers.URLField(allow_null=True, required=False)
    availability_note = serializers.CharField(allow_null=True, required=False)

class MovieDetailResponseSerializer(serializers.Serializer):
    movie_id = serializers.IntegerField()
    title_info = TitleInfoDisplayResponseSerializer()
    plot = PlotDisplayResponseSerializer()
    release_date_str = serializers.CharField()
    runtime_minutes = serializers.IntegerField()
    poster_image_url = serializers.URLField(allow_blank=True, allow_null=True) # PosterImageVO가 None일 수 있으므로
    genres = serializers.ListField(child=serializers.CharField())
    directors = serializers.ListField(child=serializers.CharField())
    cast = serializers.ListField(child=serializers.CharField())
    still_cuts = StillCutDisplayResponseSerializer(many=True)
    trailers = TrailerDisplayResponseSerializer(many=True)
    platform_ratings = MoviePlatformRatingDisplayResponseSerializer(many=True)
    ott_availability = OTTInfoDisplayResponseSerializer(many=True)
    created_at_str = serializers.CharField()
    updated_at_str = serializers.CharField(allow_null=True, required=False)