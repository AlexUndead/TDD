from django.test import TestCase
from django.contrib.auth import get_user_model
from accounts.authentication import PasswordlessAuthenticationBackend
from accounts.models import Token

User = get_user_model()


class AuthenticateTest(TestCase):
    """тест аутентификации"""

    def test_returns_None_if_no_such_token(self):
        """тест: возвращается None, если нет такого маркера"""
        result = PasswordlessAuthenticationBackend().authenticate(
            'no-such-token'
        )
        self.assertIsNone(result)

    def test_returns_new_user_with_correct_email_if_token_exists(self):
        """тест: возвращается новый пользователь с правильной
        электронной почтой, если маркер существует"""
        email = 'Alex_Undead_92@bk.ru'
        token = Token.objects.create(email=email)
        user = PasswordlessAuthenticationBackend().authenticate(token.uid)
        new_user = User.objects.get(email=email)
        self.assertEqual(user, new_user)

    def test_returns_existing_user_with_correct_email_if_token_exists(self):
        """тест: возвращается существующий пользователь с правильной
        электронной почтой, если маркер существует"""
        email = 'Alex_Undead_92@bk.ru'
        existing_user = User.objects.create(email=email)
        token = Token.objects.create(email=email)
        user = PasswordlessAuthenticationBackend().authenticate(token.uid)
        self.assertEqual(user, existing_user)


class GetUserTest(TestCase):
    """тест получения пользователя"""

    def test_gets_user_by_email(self):
        """тест: получает пользователя по адресу электронной почты"""
        User.objects.create(email='test@bk.ru')
        desired_user = User.objects.create(email='Alex_Undead_92@bk.ru')
        found_user = PasswordlessAuthenticationBackend().get_user(
            'Alex_Undead_92@bk.ru'
        )
        self.assertEqual(found_user, desired_user)

    def test_return_None_if_no_user_with_that_email(self):
        """тест: возвращается None, если нет пользователя с
        таким адресом электронной почты"""
        self.assertIsNone(
            PasswordlessAuthenticationBackend().get_user('test@test.ru')
        )
