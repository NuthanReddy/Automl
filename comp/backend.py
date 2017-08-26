from .models import UserProfile


class UserAuth(object):
    @staticmethod
    def authenticate(username=None, password=None):
        try:
            user = UserProfile.objects.get(email=username)
            if user.check_password(password):
                return user
        except UserProfile.DoesNotExist:
            return None

    @staticmethod
    def get_user(user_id):
        try:
            user = UserProfile.objects.get(pk=user_id)
            if user.is_active:
                return user
        except UserProfile.DoesNotExist:
            return None

    @staticmethod
    def login(username=None, password=None):
        try:
            user = UserProfile.objects.get(username=username)
            if user.check_password(password):
                return user
        except UserProfile.DoesNotExist:
            return None
