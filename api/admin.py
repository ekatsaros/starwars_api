from django.contrib import admin

# Register your models here.
from .models import Character, Film, Starship, Vote


@admin.register(Character)
class CharacterAdmin(admin.ModelAdmin):
    list_display = ("name", "swapi_url")
    search_fields = ("name", "swapi_url")
    list_filter = ("films", "starships")


@admin.register(Film)
class FilmAdmin(admin.ModelAdmin):
    list_display = ("title", "swapi_url", "release_date")
    search_fields = ("title", "swapi_url")
    list_filter = ("release_date",)


@admin.register(Starship)
class StarshipAdmin(admin.ModelAdmin):
    list_display = ("name", "swapi_url")
    search_fields = ("name", "swapi_url")
    list_filter = ("name",)


@admin.register(Vote)
class VoteAdmin(admin.ModelAdmin):
    list_display = ("user", "character", "film", "starship", "created_at")
    search_fields = ("user__username", "character__name", "film__title", "starship__name")
    list_filter = ("created_at",)
    raw_id_fields = ("user", "character", "film", "starship")
