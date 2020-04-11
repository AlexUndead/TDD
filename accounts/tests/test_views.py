from django.test import TestCase
from unittest.mock import patch
from accounts.models import Token
import accounts.views


class SendLoginEmailViewTest(TestCase):
    """тест представления, которое отправляет
    сообщение для входа в систему"""

    def test_redirects_to_home_page(self):
        """тест: переадресуется на домашнюю страницу"""
        response = self.client.post('/accounts/login?token=abcd123')
        self.assertRedirects(response, '/')

    def test_sends_mail_to_address_from_post(self):
        """тест: отправляется сообщение на адрес из метода post"""
        self.send_mail_called = False

        def fake_send_mail(subject, body, from_email, to_list):
            """поддельная функция send_mail"""
            self.send_mail_called = True
            self.subject = subject
            self.body = body
            self.from_email = from_email
            self.to_list = to_list

        accounts.views.send_mail = fake_send_mail

        self.client.post('/accounts/send_login_email', data={
            'email': 'edith@example.com'
        })

        self.assertTrue(self.send_mail_called)
        self.assertEqual(self.subject, 'Your login link for Superlists')
        self.assertEqual(self.from_email, 'noreply@superlists')
        self.assertEqual(self.to_list, ['edith@example.com'])

    @patch('accounts.views.send_mail')
    def test_sends_mail_to_address_from_post(self, mock_send_mail):
        """тест отправляется сообщение на адрес из метода post"""
        self.client.post('/accounts/send_login_email', data={
            'email': 'edith@example.com'
        })

        self.assertEqual(mock_send_mail.called, True)
        (subject, body, from_email, to_list), kwargs = mock_send_mail.call_args
        self.assertEqual(subject, 'Your login link for Superlists')
        self.assertEqual(from_email, 'AlexUndead1992@yandex.ru')
        self.assertEqual(to_list, ['edith@example.com'])

    def test_adds_success_message(self):
        """тест: добавляется сообщение об успехе"""
        response = self.client.post('/accounts/send_login_email', data={
            'email': 'edith@example.com'
        }, follow=True)

        message = list(response.context['messages'])[0]
        self.assertEqual(
            message.message,
            "Проверьте свою почту, мы отправили Вам ссылку, \
которую можно использовать для входа на сайт."
        )
        self.assertEqual(message.tags, "success")

    def test_creates_token_associated_with_email(self):
        """тест: создается маркер, связанный с электронной почтой"""
        self.client.post('/accounts/send_login_email', data={
            'email': 'Alex_Undead_92@bk.ru'
        })
        token = Token.objects.first()
        self.assertEqual(token.email, 'Alex_Undead_92@bk.ru')

    @patch('accounts.views.send_mail')
    def test_sends_link_to_login_using_token_uid(self, mock_send_mail):
        """тест: отсылается ссылка на вход в систему, используя uid маркера"""
        self.client.post('/accounts/send_login_email', data={
            'email': 'Alex_Undead_92@bk.ru'
        })

        token = Token.objects.first()
        expected_url = f'http://testserver/accounts/login?token={token.uid}'
        (subject, body, from_email, to_list), kwargs = mock_send_mail.call_args
        self.assertIn(expected_url, body)

