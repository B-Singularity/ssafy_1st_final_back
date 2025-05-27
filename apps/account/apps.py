from django.apps import AppConfig

class AccountsConfig(AppConfig): # 또는 AccountConfig 등 실제 클래스 이름
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.account'
    label = 'account'  # ⭐️ 앱 레이블을 명시적으로 'account'로 지정
