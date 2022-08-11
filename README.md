![foodgram_workflow](https://github.com/bitbybit/foodgram-project-react/actions/workflows/foodgram_workflow.yml/badge.svg)

## Пример

* [http://foodgram.duckdns.org/](http://foodgram.duckdns.org/)

  Логин: lena@lena.com

  Пароль: lena

* [http://foodgram.duckdns.org/admin/](http://foodgram.duckdns.org/admin/)

  Логин: admin

  Пароль: admin

* [http://foodgram.duckdns.org/api/docs/](http://foodgram.duckdns.org/api/docs/)

## Установка

1. `git clone git@github.com:bitbybit/foodgram-project-react.git`

2. Заполнить файл `infra/.env` (пример в `infra/.env.example`)

```
# указываем, что работаем с postgresql
DB_ENGINE=django.db.backends.postgresql

# имя базы данных
DB_NAME=

# логин для подключения к базе данных
POSTGRES_USER=

# пароль для подключения к БД
POSTGRES_PASSWORD=

# название сервиса (контейнера)
DB_HOST=db

# порт для подключения к БД
DB_PORT=5432

# django secret key
SECRET_KEY=

# django media url
MEDIA_URL=http://food.gram/media/
```

### Docker

```bash
docker-compose -f ./infra/docker-compose.yml up -d

# docker build . -f ./backend/Dockerfile

docker-compose -f ./infra/docker-compose.yml exec web python manage.py import_csv
docker-compose -f ./infra/docker-compose.yml exec web python manage.py createsuperuser

# docker-compose -f ./infra/docker-compose.yml exec web python manage.py loaddata /app/data/fixtures.json
```

[Docker Hub](https://hub.docker.com/repository/docker/hubhubhubhub/yamdb_final)

## ТЗ

### API

[http://food.gram/api/docs/](http://food.gram/api/docs/)
