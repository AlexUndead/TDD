from django.core.mail import send_mail
from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from django.contrib import messages
from accounts.models import Token


def send_login_email(request):
    """отправить сообщение для входа в систему"""
    email = request.POST['email']
    token = Token.objects.create(email=email)
    url = request.build_absolute_uri(
        reverse('login') + '?token=' + str(token.uid)
    )
    message_body = f'Use this link to log in:\n\n{url}'
    send_mail(
        'Your login link for Superlists',
        message_body,
        'AlexUndead1992@yandex.ru',
        [email]
    )
    messages.success(
        request,
        "Проверьте свою почту, мы отправили Вам ссылку, \
которую можно использовать для входа на сайт."
    )
    return redirect('/')


def login(request):
    return redirect('/')
