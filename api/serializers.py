from rest_framework import serializers

from api.models import Character, Film, Starship, Vote


class FilmSerializer(serializers.ModelSerializer):
    """Serializer for the Film model."""

    class Meta:
        model = Film
        fields = [
            "id",
            "title",
            "swapi_url",
            "release_date",
            "data",  # Full SWAPI film response as JSON
        ]


class StarshipSerializer(serializers.ModelSerializer):
    """Serializer for the Starship model."""

    class Meta:
        model = Starship
        fields = [
            "id",
            "name",
            "swapi_url",
            "data",  # Full SWAPI starship response as JSON
        ]


class CharacterSerializer(serializers.ModelSerializer):
    """Serializer for the Character model."""

    films = FilmSerializer(many=True, read_only=True)
    starships = StarshipSerializer(many=True, read_only=True)

    class Meta:
        model = Character
        fields = [
            "id",
            "name",
            "swapi_url",
            "films",
            "starships",
            "data",  # Full SWAPI character response as JSON
        ]


class VoteSerializer(serializers.ModelSerializer):
    """Serializer for the Vote model."""

    class Meta:
        model = Vote
        fields = ["id", "user", "character", "film", "starship", "created_at"]
