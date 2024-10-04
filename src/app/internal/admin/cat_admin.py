from django.contrib import admin

from app.internal.models.cat_model import Cat, CatBreed


@admin.register(CatBreed)
class CatBreedAdmin(admin.ModelAdmin):
    pass


@admin.register(Cat)
class CatAdmin(admin.ModelAdmin):
    pass
