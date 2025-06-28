from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers.user import UserRequestSerializer, UserResponseSerializer


class UserRegisterView(APIView):
    """
    Create a new user
    """

    def post(self, request: Request) -> Response:
        """
        Create a new user
        :param request:
        :return: Response
        """
        request_serializer = UserRequestSerializer(data=request.data)
        if request_serializer.is_valid():
            user = request_serializer.save()
            response_serializer = UserResponseSerializer(user)
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)
        return Response(request_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
