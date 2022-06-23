![example workflow](https://github.com/denshvetsov/yamdb_final/actions/workflows/yamdb_workflow.yml/badge.svg)
### Cтек технологий:
[![Python](https://img.shields.io/badge/-Python-464646?style=flat&logo=Python&logoColor=56C0C0&color=008080)](https://www.python.org/)
[![Django](https://img.shields.io/badge/-Django-464646?style=flat&logo=Django&logoColor=56C0C0&color=008080)](https://www.djangoproject.com/)
[![Django REST Framework](https://img.shields.io/badge/-Django%20REST%20Framework-464646?style=flat&logo=Django%20REST%20Framework&logoColor=56C0C0&color=008080)](https://www.django-rest-framework.org/)
[![PostgreSQL](https://img.shields.io/badge/-PostgreSQL-464646?style=flat&logo=PostgreSQL&logoColor=56C0C0&color=008080)](https://www.postgresql.org/)
[![JWT](https://img.shields.io/badge/-JWT-464646?style=flat&color=008080)](https://jwt.io/)
[![Nginx](https://img.shields.io/badge/-NGINX-464646?style=flat&logo=NGINX&logoColor=56C0C0&color=008080)](https://nginx.org/ru/)
[![gunicorn](https://img.shields.io/badge/-gunicorn-464646?style=flat&logo=gunicorn&logoColor=56C0C0&color=008080)](https://gunicorn.org/)
[![Docker](https://img.shields.io/badge/-Docker-464646?style=flat&logo=Docker&logoColor=56C0C0&color=008080)](https://www.docker.com/)
[![Docker-compose](https://img.shields.io/badge/-Docker%20compose-464646?style=flat&logo=Docker&logoColor=56C0C0&color=008080)](https://www.docker.com/)
[![Docker Hub](https://img.shields.io/badge/-Docker%20Hub-464646?style=flat&logo=Docker&logoColor=56C0C0&color=008080)](https://www.docker.com/products/docker-hub)
[![GitHub%20Actions](https://img.shields.io/badge/-GitHub%20Actions-464646?style=flat&logo=GitHub%20actions&logoColor=56C0C0&color=008080)](https://github.com/features/actions)
[![Yandex.Cloud](https://img.shields.io/badge/-Yandex.Cloud-464646?style=flat&logo=Yandex.Cloud&logoColor=56C0C0&color=008080)](https://cloud.yandex.ru/)

### demo
denshvetsov/yamdb_final

[Демо версия](http://yatube.duckdns.org/admin/)

84.201.177.209
http://yatube.duckdns.org/admin/
http://yatube.duckdns.org/redoc/

### Установка
#### Требования

- Регистрация на dockerhub
- Настроенный SSH доступ к серверу по ключу с паролем
- Регистрация на GitHub
- Выделенный сервер Linux Ubuntu 20.04 с с публичным IP адресом

#### Настройка GitHub Secrets
Клонируйте репозиторий и настройте переменные GitHub secrets согласно Вашему окружению

- DOCKER_PASSWORD
- DOCKER_USERNAME
- SERVER_HOST #публичный адрес сервера для доступа по SSH
- SERVER_SUDO_USER
- SSH_KEY #Скопируйте приватный ключ с компьютера, имеющего доступ к боевому серверу: cat ~/.ssh/id_rsa
- SSH_PASSWORD
- TELEGRAM_TOKEN #токен чат бота который будет отправлять сообщение
- TELEGRAM_CHAT_ID #кому отправлять сообщение
- DB_ENGINE пример django.db.backends.postgresql
- DB_NAME #имя образа docker-compose с базой - db
- DB_POSTGRES_USER
- DB_POSTGRES_PASSWORD
- DB_HOST
- DB_PORT

#### Установка на выделенном сервере
На боевом сервере установите docker и docker-compose
Остановите службу nginx
Скопируйте файлы из директории infra в домашную папку пользователя
    docker-compose.yaml
    nginx - сохраняя стурктуру и название папок

#### Deploy автоматически при команде git push
при git pus запускается скрипт GitHub actions который выполняет автоматический deploy на сервер


### Описание проекта:

Проект YaMDb собирает отзывы пользователей на различные художественные произведения.

### Алгоритм регистрации пользователей

Пользователь отправляет POST-запрос на добавление нового пользователя с параметрами `email` и `username` на эндпоинт `/api/v1/auth/signup/`.
YaMDB отправляет письмо с кодом подтверждения (`confirmation_code`) на адрес `email`.
Пользователь отправляет POST-запрос с параметрами `username` и `confirmation_code` на эндпоинт `/api/v1/auth/token/`, в ответе на запрос ему приходит token (JWT-токен).
При желании пользователь отправляет PATCH-запрос на эндпоинт `/api/v1/users/me/` и заполняет поля в своём профайле (описание полей — в документации).

### Пользовательские роли

- Аноним — может просматривать описания произведений, читать отзывы и комментарии.
- Аутентифицированный пользователь (`user`) — может читать всё, как и Аноним, может публиковать отзывы и ставить оценки произведениям (фильмам/книгам/песенкам), может комментировать отзывы; может редактировать и удалять свои отзывы и комментарии, редактировать свои оценки произведений. Эта роль присваивается по умолчанию каждому новому пользователю.
- Модератор (`moderator`) — те же права, что и у Аутентифицированного пользователя, плюс право удалять и редактировать любые отзывы и комментарии.
- Администратор (`admin`) — полные права на управление всем контентом проекта. Может создавать и удалять произведения, категории и жанры. Может назначать роли пользователям.
- Суперюзер Django должен всегда обладать правами администратора, пользователя с правами `admin`. Даже если изменить пользовательскую роль суперюзера — это не лишит его прав администратора. Суперюзер — всегда администратор, но администратор — не обязательно суперюзер.


### Самостоятельная регистрация новых пользователей

Пользователь отправляет POST-запрос с параметрами `email` и `username` на эндпоинт `/api/v1/auth/signup/`.
Сервис YaMDB отправляет письмо с кодом подтверждения (`confirmation_code`) на указанный адрес `email`.
Пользователь отправляет POST-запрос с параметрами username и `confirmation_code` на эндпоинт `/api/v1/auth/token/`, в ответе на запрос ему приходит token (JWT-токен).
В результате пользователь получает токен и может работать с API проекта, отправляя этот токен с каждым запросом.
После регистрации и получения токена пользователь может отправить PATCH-запрос на эндпоинт `/api/v1/users/me/` и заполнить поля в своём профайле (описание полей — в документации).

### Создание пользователя администратором

Пользователя может создать администратор — через админ-зону сайта или через POST-запрос на специальный эндпоинт `api/v1/users/` (описание полей запроса для этого случая — в документации). В этот момент письмо с кодом подтверждения пользователю отправлять не нужно.
После этого пользователь должен самостоятельно отправить свой `email` и username на эндпоинт `/api/v1/auth/signup/` , в ответ ему должно прийти письмо с кодом подтверждения.
Далее пользователь отправляет POST-запрос с параметрами `username` и `confirmation_code` на эндпоинт `/api/v1/auth/token/`, в ответе на запрос ему приходит `token` (JWT-токен), как и при самостоятельной регистрации.

### Ресурсы API YaMDb

- Ресурс `auth`: аутентификация.
- Ресурс `users`: пользователи.
- Ресурс `titles`: произведения, к которым пишут отзывы (определённый фильм, книга или песенка).
- Ресурс `categories`: категории (типы) произведений («Фильмы», «Книги», «Музыка»).
- Ресурс `genres`: жанры произведений. Одно произведение может быть привязано к нескольким жанрам.
- Ресурс `reviews`: отзывы на произведения. Отзыв привязан к определённому произведению.
- Ресурс `comments`: комментарии к отзывам. Комментарий привязан к определённому отзыву.
Каждый ресурс описан в документации Redoc: указаны эндпоинты (адреса, по которым можно сделать запрос), разрешённые типы запросов, права доступа и дополнительные параметры, если это необходимо.

### Authentication
#### jwt-token
Используется аутентификация с использованием JWT-токенов

| Security Scheme Type   | API Key |
|------------------------|--------:|
| Header parameter name  |Bearer   |

##### Автор [Денис Швецов](https://github.com/denshvetsov)
