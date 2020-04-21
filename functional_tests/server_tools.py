from fabric.api import run
from fabric.context_managers import settings


def _get_manage_dot_py():
    """получить manage.py"""
    return f'~/sites/TDD-staging/virtualenv/bin/python ~/sites/TDD-staging/source/manage.py'


def reset_database():
    """обнулить базу данных"""
    manage_dot_py = _get_manage_dot_py()
    with settings(host_string=f'ubuntu@18.221.14.125'):
        run(f'{manage_dot_py} flush --noinput')


def create_session_on_server(email):
    """создать сеанс на сервере"""
    manage_dot_py = _get_manage_dot_py()
    with settings(host_string=f'ubuntu@18.221.14.125'):
        session_key = run(f'{manage_dot_py} create_session {email}')
        return session_key.strip()
