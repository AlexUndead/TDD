from django.core import mail
from django.conf import settings
from selenium.webdriver.common.keys import Keys
import re
import os
import poplib
import time

from .base import FunctionalTest

TEST_EMAIL = settings.EMAIL_TEST_YANDEX_USER
TEST_PASSWORD = settings.EMAIL_TEST_YANDEX_PASSWORD
SUBJECT = 'Your login link for Superlists'


class LoginTest(FunctionalTest):
    """тест регистрации в системе"""

    def test_can_get_email_link_to_log_in(self):
        """тест: можно получить ссылку по почте для регистрации"""
        # Эдит заходит на офигительный сайт супесписков и впервые
        # замечает раздел "войти" в навигациооной панели
        # Он говорит ей ввести свой адрес электронной почты, что она и делает
        self.browser.get(self.live_server_url)
        self.browser.find_element_by_name('email').send_keys(TEST_EMAIL)
        self.browser.find_element_by_name('email').send_keys(Keys.ENTER)

        # Появляется сообщение, которое говорит, что ей на почту
        # было выслано электронное письмо
        self.wait_for(lambda: self.assertIn(
            'Проверьте свою почту',
            self.browser.find_element_by_tag_name('body').text
        ))

        # Эдит проверяет свою почту и находит сообщение
        body = self.wait_for_email(TEST_EMAIL, SUBJECT)

        # Оно содержит ссылку на url-адрес
        self.assertIn('Use this link to log in', body)
        url_search = re.search(r'http://.+/.+$', body)
        if not url_search:
            self.fail(f'Could not find url in email body:\n{body}')
        url = url_search.group(0)
        self.assertIn(self.live_server_url, url)

        # Эдит нажимает на ссылку
        self.browser.get(url)

        # Она зарегистрирована в системе!
        self.wait_to_be_logged_in(email=TEST_EMAIL)

        # Теперь она выходит из системы
        self.browser.find_element_by_link_text('Log out').click()

        # Она вышла из системы
        self.wait_to_be_logged_out(email=TEST_EMAIL)

    def wait_for_email(self, test_email, subject):
        """ожидать электронное сообщение"""
        if not self.staging_server:
            email = mail.outbox[0]
            self.assertIn(test_email, email.to)
            self.assertEqual(email.subject, subject)
            return email.body

        email_id = None
        start = time.time()
        inbox = poplib.POP3_SSL('pop.yandex.ru')
        try:
            inbox.user(TEST_EMAIL)
            inbox.pass_(TEST_PASSWORD)
            while time.time() - start < 5:
                # получить 10 самых новых сообщений
                count, _ = inbox.stat()
                for i in reversed(range(max(1, count - 10), count + 1)):
                    print('getting msg', i)
                    _, lines, __ = inbox.retr(i)
                    lines = [l.decode('utf8') for l in lines]
                    if f'Subject: {subject}' in lines:
                        email_id = i
                        body = '\n'.join(lines)
                        return body
                time.sleep(5)
        finally:
            if email_id:
                inbox.dele(email_id)
            inbox.quit()
