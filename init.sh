#! /bin/bash

# проект разворачиваем в home/box/web

# устанавливаем django 2.0
sudo pip3 install django==2.0

# устанавливаем зависимости
sudo pip3 install pathlib

# копируем конфиг nginx в директорию nginx
sudo cp ~/stepic_web_old_django/nginx.conf /etc/nginx/nginx.conf

# копируем директорию проекта
sudo cp -R ~/stepic_web_old_django ~/web

# Запускаем nginx
sudo /etc/init.d/nginx start
sudo nginx -s reload

# Создание таблиц в Django
cd ~/web/ask
sudo python3 manage.py makemigrations
sudo python3 manage.py migrate

# Запускаем backend-сервер
cd ~/web/ask
python3 manage.py runserver 0:8000