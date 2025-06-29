from django.conf import settings
from django.db import models


class Film(models.Model):
    title = models.CharField(max_length=255)
    swapi_url = models.URLField(unique=True)
    release_date = models.DateField()
    # ... Add more fields as needed

    def __str__(self) -> str:
        return self.title


class Starship(models.Model):
    name = models.CharField(max_length=255)
    swapi_url = models.URLField(unique=True)
    data = models.JSONField()  # Stores the full SWAPI starship response as JSON

    def __str__(self) -> str:
        return self.name


class Character(models.Model):
    name = models.CharField(max_length=255)
    swapi_url = models.URLField(unique=True)
    films = models.ManyToManyField(Film, related_name="characters")
    starships = models.ManyToManyField(Starship, related_name="characters", blank=True)
    data = models.JSONField()  # Stores the full SWAPI character response as JSON

    def __str__(self) -> str:
        return self.name


class Vote(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    character = models.ForeignKey("Character", null=True, blank=True, on_delete=models.CASCADE)
    film = models.ForeignKey("Film", null=True, blank=True, on_delete=models.CASCADE)
    starship = models.ForeignKey("Starship", null=True, blank=True, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        # Prevents a user from voting more than once on the same item
        constraints = [
            models.UniqueConstraint(fields=["user", "character"], name="unique_user_character_vote"),
            models.UniqueConstraint(fields=["user", "film"], name="unique_user_film_vote"),
            models.UniqueConstraint(fields=["user", "starship"], name="unique_user_starship_vote"),
        ]
