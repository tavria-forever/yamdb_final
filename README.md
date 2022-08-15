# Проект «API для YamDB»

![yamdb_final workflow status](https://github.com/tavria-forever/yamdb_final/actions/workflows/yamdb_workflow.yml/badge.svg)

[YamDB API](http://51.250.100.230/redoc/) - лучший каталог фильмов в интернете.

## Docker образ

Доступен всем по на [dockerhub](https://hub.docker.com/repository/docker/tavriaforever/yamdb_final).

## Шаблон наполнения env-файла

```shell
DB_ENGINE=django.db.backends.postgresql # указываем, что работаем с postgresql
DB_NAME=postgres # имя базы данных
POSTGRES_USER=postgres # логин для подключения к базе данных
POSTGRES_PASSWORD=postgres # пароль для подключения к БД (установите свой)
DB_HOST=db # название сервиса (контейнера)
DB_PORT=5432 # порт для подключения к БД
DJANGO_SECRET_KEY=5555
DJANGO_DEBUG=False
```

## Oписание команд для запуска приложения в контейнерах

### Запустить сервер
```shell
cd infra/
docker-compose up --build
```

Когда вы запустите проект, по адресу http://localhost/redoc/ будет доступна документация для API YamDB. В документации описано, какие доступны ручки в API. Документация представлена в формате Redoc.

# Регистрация

1. Пользователь отправляет POST-запрос на добавление нового пользователя с параметрами `email` и `username` на эндпоинт `/api/v1/auth/signup/`.
YaMDB отправляет письмо с кодом подтверждения (`confirmation_code`) на адрес `email`.

**n.b.** Код подтверждения на `email`, при разработке его можно увидеть в консоле, где запущен сервер.

2. Пользователь отправляет POST-запрос с параметрами `username` и `confirmation_code` на эндпоинт `/api/v1/auth/token/`, в ответе на запрос ему приходит `token` (`JWT-токен`).
При желании пользователь отправляет PATCH-запрос на эндпоинт `/api/v1/users/me/` и заполняет поля в своём профайле (описание полей — в документации).

3. Для эндпоинтов, которые требуют авторизации, указать в качестве заголовка:
```
Bearer <ваш токен>
```

### Остановить сервер

```shell
cd infra/
docker-compose down -v
```

## Описание команды для заполнения базы данными

Запустить `docker-compose` из папки `infra`.

1. Получить дамп данных в JSON.

```shell
cd api_yamdb/
docker-compose exec web python manage.py dumpdata > fixtures.json
```

2. Заполнить базу данных новыми фикстурами

```shell
docker-compose exec web python manage.py loaddata fixtures.json
```

3. Выполнить миграцию

```shell
docker-compose exec web python manage.py migrate
```

4. Собрать всю статику в одну папку

```shell
docker-compose exec web pythonmanage.py collectstatic --no-input
```

Для удобства шаги автоматизированы и будут выполнены при запуске `docker-compose` из файла `api_yamdb/docker-start.sh`.

## CI

Для удобства разработки и деплоя, настроен CI через github actions. Конфиг лежит в директории [.github/workflows/yamdb_workflow.yml](./.github/workflows/yamdb_workflow.yml).

При каждом push в ветку master:
- линтинг файлов с помощью Flake8;
- прогон тестов pytest;
- сборка и загрузка докер образа в свой репозиторий;
- деплой проекта на боевой сервер.

## Автор проекта

По всем вопросам и предложениям можно писать Николаю Ильченко на [почту](tavriaforever@yandex.ru). 
