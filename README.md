<a href="https://practicum.yandex.ru/" align="center">
    <div>
        <img src="https://yastatic.net/q/logoaas/v2/Яндекс.svg?circle=white&amp;color=fff&amp;first=black">
        <img src="https://yastatic.net/q/logoaas/v2/Практикум.svg?color=fff">
    </div>
</a>

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Django](https://img.shields.io/badge/django-%23092E20.svg?style=for-the-badge&logo=django&logoColor=white)
![DjangoREST](https://img.shields.io/badge/DJANGO-REST-ff1709?style=for-the-badge&logo=django&logoColor=white&color=ff1709&labelColor=gray)
![YAML](https://img.shields.io/badge/yaml-%23ffffff.svg?style=for-the-badge&logo=yaml&logoColor=151515)
![PyCharm](https://img.shields.io/badge/pycharm-143?style=for-the-badge&logo=pycharm&logoColor=black&color=black&labelColor=green)
![Notepad++](https://img.shields.io/badge/Notepad++-90E59A.svg?style=for-the-badge&logo=notepad%2b%2b&logoColor=black)
![Google Chrome](https://img.shields.io/badge/Google%20Chrome-4285F4?style=for-the-badge&logo=GoogleChrome&logoColor=white)
![React](https://img.shields.io/badge/react-%2320232a.svg?style=for-the-badge&logo=react&logoColor=%2361DAFB)
![SQLite](https://img.shields.io/badge/sqlite-%2307405e.svg?style=for-the-badge&logo=sqlite&logoColor=white)
![Postgres](https://img.shields.io/badge/postgres-%23316192.svg?style=for-the-badge&logo=postgresql&logoColor=white)
![Postman](https://img.shields.io/badge/Postman-FF6C37?style=for-the-badge&logo=postman&logoColor=white)
![Gunicorn](https://img.shields.io/badge/gunicorn-%298729.svg?style=for-the-badge&logo=gunicorn&logoColor=white)
![Nginx](https://img.shields.io/badge/nginx-%23009639.svg?style=for-the-badge&logo=nginx&logoColor=white)
![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white)
![DockerHub](https://img.shields.io/badge/docker.hub-%230fed.svg?style=for-the-badge&logo=docker&logoColor=white)
![GitHub](https://img.shields.io/badge/github-%23121011.svg?style=for-the-badge&logo=github&logoColor=white)
![GitHub Actions](https://img.shields.io/badge/github%20actions-%232671E5.svg?style=for-the-badge&logo=githubactions&logoColor=white)
![Telegram](https://img.shields.io/badge/Telegram_BOT-2CA5E0?style=for-the-badge&logo=telegram&logoColor=white)

# Дипломный проект факультета бэкэнд-разработки 75 когорта
<a href="https://foodgram.kokor.in/"> 
    <H2 align="center">Foodgram </H2>
</a>

### Описание проекта: 
#### Проект «Фудграм» — сайт, на котором пользователи могут публиковать рецепты, добавлять чужие рецепты в избранное и подписываться на публикации других авторов. Пользователям сайта также доступен сервис «Список покупок». Он позволяет создавать список продуктов, которые нужно купить для приготовления выбранных блюд.

### Структура проекта
#### Проект представляет собой API на Django + DRF, OSP  на react, СУБД PostgreSQL, в качестве web-сервера используется NGINX. Все сервисы развернуты в Docker-контейнерах, Docker-файлы сервисов находятся в соответствующих папках проекта


### API
#### Описание ресурсов, методов и ответов API доступно по адресу : <a href="https://foodgram.kokor.in/redoc">https://foodgram.kokor.in/redoc<a/>

### Развертывание проекта локально
#### 1. Необходимо клонировать репозиторий
```
git clone git@github.com:kokorink/foodgram-project-react.git
```
#### 2. Создать и заполнить файл .env в корневой дирректории проекта
#### Пример файла ```.env_exapmle```

Значение параметра ```DEBUG``` влияет на использование БД

```True``` - SQLite3

```False``` - PostgreSQL

#### 3.1 Запуск на встроенном сервере разработки Django
```
cd backend
```
Cоздать и активировать виртуальное окружение

```
python3 -m venv env
source env/bin/activate
python3 -m pip install --upgrade pip
```
Установить зависимости из файла requirements.txt
```
pip install -r requirements.txt
```
Выполнить миграции
```
python3 manage.py makemigrations
python3 manage.py migrate
```
Добавить в БД данные об ингридиентах и тэгах
```
python3 manage.py dataload
```
Запустить проект
```
python3 manage.py runserver
```

### 3.2 Запуск проекта локально в Docker-контейнерах
Создание образов, запуск контейнеров, создание и подключение томов
```
docker compose up
```
Выполнить миграции
```
docker compose up exec backend python3 manage.py makemigrations
docker compose up exec backend python3 manage.py migrate
```
Добавить в БД данные об ингридиентах и тэгах
```
docker compose up exec python3 manage.py dataload
```
Подключить статику для бэкэнда
```
docker compose up exec backend python3 manage.py collectstatic
docker compose up exec backend cp -r static/. ../backend_static/static/
```
### 3.3 Запуск проекта на удалённом сервере в продакшн
#### Автоматизации доставки и развертывания приложения на удалённом сервере реализована с помощью GitHub Actions и DockerHub
#### WorkFlow находится в папке ```.github/workflows/```

Для развётрывания на удалённом сервере необходимо в папку ```/home/{user_name}/dev/projects/foodgram``` 
скопировать файл ```.env```

Для автоматической загрузки обновления образов иразвертывания на удалённом сервере необходимо 
на GitHub добавить следующие секретные переменные репозитория: 
```
DOCKER_USERNAME - login учётной записи на Docker.com
DOCKER_PASSWORD - пароль от учётной записи на Docker.com
HOST - IP-адрес удалённого сервера
USER - login учётной записи на удалённом сервере
SSH_KEY - приватный ключ доступа по SSH на удалённый сервер
SSH_PASSPHRASE - пароль от приватного ключа для доступа по SSH на удалённый сервер
```
Для информирования об удачном деплое на удалённом сервере обновления предуствотрено оповещени посредством Telegram.
Для этого необходимо в secrets внести ещё 2 значения:
```
TELEGRAM_TO - ID получателя Telegram (можно узнать в боте @userinfobot)
TELEGRAM_TOKEN - токен доступа Telegram (можно получить в боте @BotFather)
```

### Автор проекта: Константин Кокорин
#### Студент 75 когорты курса Python-разработчик Яндекс.Практикум

### Ревьювер: Александр Дурнев


### © Copyright
#### All rights reserved
