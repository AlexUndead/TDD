# import sys
from .models import Token, User


class PasswordlessAuthenticationBackend:
    """беспарольный серверный процессор аутентификации"""

    def authenticate(self, uid):
        """аутентифицировать"""
        try:
            token = Token.objects.get(uid=uid)
            return User.objects.get(email=token.email)
        except User.DoesNotExist:
            return User.objects.create(email=token.email)
        except Token.DoesNotExist:
            return None
        # """аутентифицировать"""
        # print('uid', uid, file=sys.stderr)
        # if not Token.objects.filter(uid=uid).exists():
        #     print('no token found', file=sys.stderr)
        #     return None
        # token = Token.objects.get(uid=uid)
        # print('got token', file=sys.stderr)
        # try:
        #     user = ListUser.objects.get(email=token.email)
        #     print('got user', file=sys.stderr)
        #     return user
        # except ListUser.DoesNotExist:
        #     print('new user', file=sys.stderr)
        #     return ListUser.objects.create(email=token.email)

    def get_user(self, email):
        """получить пользователя"""
        # return ListUser.objects.get(email=email)
        try:
            return User.objects.get(email=email)
        except User.DoesNotExist:
            return None
