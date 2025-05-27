from django.apps import AppConfig

class ContentManagementConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.content_management'
    # verbose_name = "콘텐츠 관리" # 선택 사항: Django 관리자 등에서 표시될 이름