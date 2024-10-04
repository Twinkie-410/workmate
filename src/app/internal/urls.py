from django.urls import include, path

urlpatterns = [
    path("users/", include("app.internal.urls-paths.user_urls")),
    path("auth/", include("app.internal.urls-paths.auth_urls")),
    path("cats/", include("app.internal.urls-paths.cat_urls")),
]
