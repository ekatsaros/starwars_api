from django.contrib.auth import get_user_model
from django.db import transaction
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from api.models import Character, Film, Starship, Vote

User = get_user_model()


class FilmApiViewTests(APITestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        self.user = User.objects.create_user(
            first_name="Test", last_name="Tester", email="test@email.com", username="testuser", password="testpass"
        )
        self.client.force_authenticate(user=self.user)
        self.film = Film.objects.create(
            title="Test Film",
            swapi_url="https://swapi.dev/api/films/1/",
            release_date="2023-01-01",
            data={"title": "Test Film", "url": "https://swapi.dev/api/films/1/"},
        )
        Film.objects.create(
            title="Another Film",
            swapi_url="https://swapi.dev/api/films/2/",
            release_date="2023-02-01",
            data={"title": "Another Film", "url": "https://swapi.dev/api/films/2/"},
        )

    def test_fetch_films(self) -> None:
        url = reverse("film-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["films"]), 2)

    def test_fetch_film_by_name(self) -> None:
        url = reverse("film-list")
        response = self.client.get(url, {"search": "Test Film"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["films"]), 1)
        self.assertEqual(response.data["films"][0]["title"], "Test Film")


class CharacterApiViewTests(APITestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        self.user = User.objects.create_user(
            first_name="Test", last_name="Tester", email="test@email.com", username="testuser", password="testpass"
        )
        self.client.force_authenticate(user=self.user)
        self.character = Character.objects.create(
            name="Test Character",
            swapi_url="https://swapi.dev/api/people/1/",
            data={
                "name": "Test Character",
                "height": "180",
                "mass": "80",
                "hair_color": "brown",
                "occupation": "Jedi",
                "url": "https://swapi.dev/api/people/1/",
                "films": ["https://swapi.dev/api/films/1/"],
                "starships": ["https://swapi.dev/api/starships/1/"],
            },
        )
        Character.objects.create(
            name="Another Character",
            swapi_url="https://swapi.dev/api/people/2/",
            data={
                "name": "Another Character",
                "height": "170",
                "mass": "70",
                "hair_color": "blonde",
                "occupation": "Pilot",
                "url": "https://swapi.dev/api/people/2/",
                "films": ["https://swapi.dev/api/films/2/"],
                "starships": ["https://swapi.dev/api/starships/2/"],
            },
        )

    def test_fetch_characters(self) -> None:
        url = reverse("character-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["characters"]), 2)

    def test_fetch_character_by_name(self) -> None:
        url = reverse("character-list")
        response = self.client.get(url, {"search": "Test Character"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["characters"]), 1)
        self.assertEqual(response.data["characters"][0]["name"], "Test Character")


class StarshipApiViewTests(APITestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        self.user = User.objects.create_user(
            first_name="Test", last_name="Tester", email="test@email.com", username="testuser", password="testpass"
        )
        self.client.force_authenticate(user=self.user)
        self.starship = Starship.objects.create(
            name="Test Starship",
            swapi_url="https://swapi.dev/api/starships/1/",
            data={"name": "Test Starship", "url": "https://swapi.dev/api/starships/1/"},
        )
        Starship.objects.create(
            name="Another Starship",
            swapi_url="https://swapi.dev/api/starships/2/",
            data={"name": "Another Starship", "url": "https://swapi.dev/api/starships/2/"},
        )

    def test_fetch_starships(self) -> None:
        url = reverse("starship-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["starships"]), 2)

    def test_fetch_starship_by_name(self) -> None:
        url = reverse("starship-list")
        response = self.client.get(url, {"search": "Test Starship"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["starships"]), 1)
        self.assertEqual(response.data["starships"][0]["name"], "Test Starship")


class VoteApiViewTests(APITestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        self.user = User.objects.create_user(
            first_name="Test", last_name="Tester", email="test@email.com", username="testuser", password="testpass"
        )
        self.client.force_authenticate(user=self.user)
        self.film = Film.objects.create(
            title="Test Film",
            swapi_url="https://swapi.dev/api/films/1/",
            release_date="2023-01-01",
            data={"title": "Test Film", "url": "https://swapi.dev/api/films/1/"},
        )

    def test_vote_for_film(self) -> None:
        url = reverse("vote-create")
        response = self.client.post(
            url, data={"film": self.film.id, "character": None, "starship": None}, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Vote.objects.count(), 1)
        url = reverse("film-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["films"][0]["votes"], 1)

    def test_vote_cannot_vote_twice(self) -> None:
        url = reverse("vote-create")
        self.client.post(url, data={"film": self.film.id, "character": None, "starship": None}, format="json")
        with transaction.atomic():  # Ensure atomicity for the test due to assertions during the transaction
            response = self.client.post(
                url, data={"film": self.film.id, "character": None, "starship": None}, format="json"
            )
        self.assertEqual(response.status_code, status.HTTP_409_CONFLICT)
        self.assertEqual(Vote.objects.count(), 1)
        self.assertEqual(response.data["error"], "You have already voted for an item.")
        self.assertEqual(response.data["detail"], "UNIQUE constraint failed: api_vote.user_id, api_vote.film_id")
