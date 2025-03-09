from users.models import Users


class BaseUserDAO:

    @staticmethod
    def get_user_by_username(username):
        try:
            return Users.objects.get(username=username)
        except Users.DoesNotExist:
            return None
        
class UserDAO(BaseUserDAO):
    pass