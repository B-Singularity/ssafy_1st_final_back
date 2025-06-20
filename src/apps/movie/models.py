from django.db import models

# Create your models here.

class GenreModel(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

class PersonModel(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, unique=True)
    external_id = models.CharField(max_length=100, null=True, blank=True, unique=True)

    def __str__(self):
        return self.name


class MovieModel(models.Model):
    id = models.AutoField(primary_key=True)
    korean_title = models.CharField(max_length=255)
    original_title = models.CharField(max_length=255, null=True, blank=True)
    plot = models.TextField(null=True, blank=True)
    release_date = models.DateField(null=True, blank=True)
    runtime_minutes = models.IntegerField(null=True, blank=True)
    poster_image_url = models.URLField(max_length=1024, null=True, blank=True)

    genres = models.ManyToManyField(GenreModel, related_name="movies")
    directors = models.ManyToManyField(PersonModel, related_name="directed_movies")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "movies"
        verbose_name = "영화"
        verbose_name_plural = "영화 목록"

    def __str__(self):
        return self.korean_title

class MovieCastMemberModel(models.Model):
    id = models.AutoField(primary_key=True)
    movie = models.ForeignKey(MovieModel, on_delete=models.CASCADE, related_name="cast_members")
    actor = models.ForeignKey(PersonModel, on_delete=models.CASCADE, related_name="filmography")
    role_name = models.CharField(max_length=100, null=True, blank=True)

    class Meta:
        db_table = "movie_cast_members"
        unique_together = ('movie', 'actor', 'role_name')
        verbose_name = "영화 출연진"
        verbose_name_plural = "영화 출연진 목록"

    def __str__(self):
        return f"{self.actor.name} as {self.role_name} in {self.movie.korean_title}"

class StillCutModel(models.Model):
    id = models.AutoField(primary_key=True)
    movie = models.ForeignKey(MovieModel, on_delete=models.CASCADE, related_name="still_cuts")
    image_url = models.URLField(max_length=1024)
    caption = models.CharField(max_length=255, null=True, blank=True)
    display_order = models.IntegerField(default=0)

    class Meta:
        db_table = "movie_still_cuts"
        ordering = ['display_order']
        verbose_name = "영화 스틸컷"
        verbose_name_plural = "영화 스틸컷 목록"

class TrailerModel(models.Model):
    id = models.AutoField(primary_key=True)
    movie = models.ForeignKey(MovieModel, on_delete=models.CASCADE, related_name="trailers")
    url = models.URLField(max_length=1024)
    trailer_type = models.CharField(max_length=50, null=True, blank=True)
    site_name = models.CharField(max_length=50, null=True, blank=True)
    thumbnail_url = models.URLField(max_length=1024, null=True, blank=True)

    class Meta:
        db_table = "movie_trailers"
        verbose_name = "영화 예고편"
        verbose_name_plural = "영화 예고편 목록"

class MoviePlatformRatingModel(models.Model):
    id = models.AutoField(primary_key=True)
    movie = models.ForeignKey(MovieModel, on_delete=models.CASCADE, related_name="platform_ratings")
    platform_name = models.CharField(max_length=100)
    score = models.FloatField() # 0.0 ~ 10.0 가정

    class Meta:
        db_table = "movie_platform_ratings"
        unique_together = ('movie', 'platform_name')
        verbose_name = "플랫폼별 영화 평점"
        verbose_name_plural = "플랫폼별 영화 평점 목록"


class OTTPlatformModel(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, unique=True)
    logo_image_url = models.URLField(max_length=1024, null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "ott_platforms"
        verbose_name = "OTT 플랫폼"
        verbose_name_plural = "OTT 플랫폼 목록"

class MovieOTTAvailabilityModel(models.Model):
    id = models.AutoField(primary_key=True)
    movie = models.ForeignKey(MovieModel, on_delete=models.CASCADE, related_name="ott_availability")
    platform = models.ForeignKey(OTTPlatformModel, on_delete=models.CASCADE, related_name="available_movies")
    watch_url = models.URLField(max_length=1024, null=True, blank=True)
    availability_note = models.CharField(max_length=100, null=True, blank=True)

    class Meta:
        db_table = "movie_ott_availability"
        unique_together = ('movie', 'platform')
        verbose_name = "영화 OTT 시청 정보"
        verbose_name_plural = "영화 OTT 시청 정보 목록"

