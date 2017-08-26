from .models import UserProfile


class UserAuth(object):
    def authenticate(self, username=None, password=None):
        try:
            user = UserProfile.objects.get(email=username)
            if user.check_password(password):
                return user
        except UserProfile.DoesNotExist:
            return None

        def get_user(self, user_id):
            try:
                user = UserProfile.objects.get(pk=user_id)
                if user.is_active:
                    return user
            except UserProfile.DoesNotExist:
                return None
