Обеспечение работы нового сайта
================================
## Необходимые пакеты:
* nginx
* Python 3.6
* virtualenv + pip
* Git


	sudo apt-get install nginx git python36 python3.6-venv


## Конфигурация виртуального узла Nginx

* см. nginx.template.conf
* заменить SITENAME, например, на TDD-staging

## Служба System

* см. gunicorn-systemd.template.service
* заменить SITENAME, например, на TDD-staging

## Структура папок:

/home/username
--sites
  --SITENAME
    --database
    --source
    --static
    --virtualenv
