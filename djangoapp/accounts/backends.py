from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from .models import User


class EmailAndUsernameBackend(ModelBackend):

    def authenticate(self, request, username=None, password=None, **kwargs):

        UserModel = User

        if username is None:
            username = kwargs.get(UserModel.USERNAME_FIELD)
        try:
            user = UserModel.objects.get(
                Q(email=username) | Q(username=username))
        except UserModel.DoesNotExist:
            UserModel().set_password(password)
        else:
            if user.check_password(password) and self.user_can_authenticate(user):

                return user
