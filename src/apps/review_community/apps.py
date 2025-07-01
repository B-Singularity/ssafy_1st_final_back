from django.apps import AppConfig

class ReviewCommunityConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'src.apps.review_community'
    # verbose_name = "리뷰 및 커뮤니티" # 선택 사항
    label = 'review_community'