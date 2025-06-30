from django.urls import path

from api.views import CharacterApiView, FilmApiView, StarshipApiView, VoteApiView

urlpatterns = [
    path("films/", FilmApiView.as_view(), name="film-list"),
    path("characters/", CharacterApiView.as_view(), name="character-list"),
    path("starships/", StarshipApiView.as_view(), name="starship-list"),
    path("votes/", VoteApiView.as_view(), name="vote-create"),
]
