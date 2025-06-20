from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    # ✅ 'apps.'로 시작하는 올바른 경로 사용
    path('api/accounts/', include('apps.account.interface.urls')),
    path('api/movies/', include('apps.movie.interface.web.urls')),
    path('api/community/', include('apps.review_community.interface.urls')),
]