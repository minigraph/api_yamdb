# Проект Api_yamdb
### Описание
Перед Вами API проекта YaMDB (Ya Movie DataBase). Учебный проект Яндекс.Практикум.
Проект ставит перед собой цели создания базы произведений и их рейтинг на основе оценки пользователей, по средствам отзывов, возможности комментаривать эти отзывы. Пользователя имеет возможность регистрации и внесения некоторых личных данных, публикации отзывов и присвоения оценки, просмотр чужих отзывов и написание комментариев к ним.
Проект реализован через архитектуру SPA. В данной части проекта реализован backend приложения по средствам Django Rest Framework.
использовано:
* Python v.3.7.5 (https://docs.python.org/3.7/)
* Django v.2.2.16 (https://docs.djangoproject.com/en/2.2/)
* DRF v.3.12.4 (https://www.django-rest-framework.org/community/release-notes/#312x-series)
* Simple JWT v.4.7.2 (https://django-rest-framework-simplejwt.readthedocs.io/en/latest/)
* Flake 8 v.5.0.4 (https://buildmedia.readthedocs.org/media/pdf/flake8/stable/flake8.pdf)

### Установка:
Клонировать репозиторий и перейти в него в командной строке:

```
git clone https://github.com/minigraph/api_yamdb.git
```

```
cd api_yamdb
```

Cоздать и активировать виртуальное окружение:

```
python3 -m venv env
```

```
source env/bin/activate
```

Обновите PIP, дабы избежать ошибок установки зависимостей:

```
python3 -m pip install --upgrade pip
```

Установить зависимости из файла requirements.txt:

```
pip install -r requirements.txt
```

Выполнить миграции:

```
python3 manage.py migrate
```

Запустить проект:

```
python3 manage.py runserver
```

### Примеры запросов:
##### Получение данных своего профиля
```
GET http://127.0.0.1:8000/api/v1/users/me/
```
Результат запроса:
```json
{
  "username": "Luen",
  "email": "test@test.ru",
  "first_name": "Luen",
  "last_name": "",
  "bio": "",
  "role": "moderator"
}
```

##### Получение списка всех пользователей с токеном модератора
```
http://127.0.0.1:8000/api/v1/users/
```
Результат запроса:
```json
{
    "detail": "You do not have permission to perform this action."
}
```

##### Получение списка всех пользователей с токеном администратора
```
http://127.0.0.1:8000/api/v1/users/
```
Результат запроса:
```json
{
  "count": 2,
  "next": null,
  "previous": null,
  "results": [
    {
      "username": "admin",
      "email": "admin@gmail.com",
      "first_name": "Админ",
      "last_name": "Админский",
      "bio": "",
      "role": "user"
    },
    {
      "username": "Luen",
      "email": "test@test.ru",
      "first_name": "Luen",
      "last_name": "",
      "bio": "",
      "role": "moderator"
    },
}
```
##### Запрос получения списка отзывов:
```
GET http://127.0.0.1:8000/api/v1/titles/{title_id}/reviews/
```
Ответ:
```
Status code: 200
```
```json
{
  "count": 123,
  "next": "http://127.0.0.1:8000/api/v1/titles/1/reviews/?page=2",
  "previous": null,
  "results": [
    {
       "id": 0,
        "text": "string",
        "author": "string",
        "score": 1,
        "pub_date": "2022-08-24T14:15:22Z",
        "title": 1
    }
  ]
}
```

##### Запрос добавления комментария:
```
POST http://127.0.0.1:8000/api/v1/titles/{title_id}/reviews/{review_id}/comments/
```
Данные:
```json
{
  "text": "string"
}
```
Ответы:
```
Status code: 200
```
```json
{
  "id": 0,
  "author": "string",
  "text": "string",
  "pub_date": "2022-08-24T14:15:22Z",
}
```
```
Status code: 400
```
```json
{
  "text": [
    "Обязательное поле."
  ]
}
```
```
Status code: 401
```
```json
{
  "detail": "Учетные данные не были предоставлены."
}
```
```
Status code: 404
```
```json
{
  "detail": "Страница не найдена."
}
```

##### Запрос частичного обновления комментария:
```
PATCH http://127.0.0.1:8000/api/v1/titles/{title_id}/reviews/{review_id}/comments/{comment_id}/
```
Данные:
```json
{
  "text": "string"
}
```
Ответы:
```
Status code: 200
```
```json
{
  "id": 0,
  "author": "string",
  "text": "string",
  "pub_date": "2022-08-24T14:15:22Z",
}
```
```
Status code: 401
```
```json
{
  "detail": "Учетные данные не были предоставлены."
}
```
```
Status code: 403
```
```json
{
  "detail": "У вас недостаточно прав для выполнения данного действия."
}
```
```
Status code: 404
```
```json
{
  "detail": "Страница не найдена."
}
```

Подробная инструкция после установки и запуска проекта по адресу:
[Документация ReDoc](http://127.0.0.1:8000/redoc/)

### Авторы:
* Андрей Макарочкин
* * e-mail: makarochkin.a.v@yandex.ru;
* Оксана Невская
* * tlg: @Luen96 
* * e-mail: luen96@yandex.ru;
* Михаил Никитин
* * tlg: @minigraf 
* * e-mail: minigraph@yandex.ru; maikl.nikitin@yahoo.com;
