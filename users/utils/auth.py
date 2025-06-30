from rest_framework.authtoken.models import Token
from rest_framework.exceptions import AuthenticationFailed

from ..models import ApiUser as User


def get_user_from_token(token: str) -> User:
    """
    Helper function to get user from token
    :param token:
    :return: User
    """
    try:
        return Token.objects.get(key=token.removeprefix("Token").strip(" ")).user
    except Token.DoesNotExist:
        raise AuthenticationFailed("Authentication credentials were not provided.")
