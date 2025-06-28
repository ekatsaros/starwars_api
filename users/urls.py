# add urls for the users app
from django.urls import path

from users.views import UserLoginView, UserRegisterView

urlpatterns = [
    path("register/", UserRegisterView.as_view(), name="user-register"),
    path("login/", UserLoginView.as_view(), name="user-login"),
]
