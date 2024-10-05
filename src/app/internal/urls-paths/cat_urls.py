from django.urls import path

from app.internal.views.cat_view import *

urlpatterns = [
    path("create/", CatCreateAPIView.as_view(), name="cat-create"),
    path("breeds/", CatBreedListAPIView.as_view(), name="breeds"),
    path("<int:id>/", CatDetailAPIView.as_view(), name="cat-retrieve-detail"),
    path("list/", CatListAPIView.as_view(), name="cats"),
    path("list/breed", CatListByBreedAPIView.as_view(), name="cats-breed"),
    # path("<int:id>/", CatUpdateDestroyAPIView.as_view(), name="cat-update-delete"),
]
