
from users.models import Users


def authenticate_by_email(email, password):
    try:
        user = Users.objects.get(email=email)
        if user.check_password(password):
            return user
        else:
            return None
    except Exception:
        return None