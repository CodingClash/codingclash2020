from django.contrib import admin
from django.urls import include, path


urlpatterns = [
    path('admin/', admin.site.urls),
    path("", include("codingclash.apps.auth.urls", namespace="auth")),
    path("", include("codingclash.apps.dashboard.urls", namespace="dashboard")),
    path("", include("codingclash.apps.games.urls", namespace="games")),
    path("oauth/", include("social_django.urls", namespace="social"))
]
