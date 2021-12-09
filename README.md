
# API_YaMDB

### Описание
API для проекта YaMDB - социальной сети, которая собирает отзывы и оценки пользователей на произведения в разных категориях и жанрах.

Для авторизации используется код подтверждения.
Для аутентификации используются JWT-токены. 

### Как запустить проект:
Клонировать репозиторий и перейти в него в командной строке:

```
git clone https://github.com/Seniacat/api_yamdb.git
```

Cоздать и активировать виртуальное окружение:

```
python3 -m venv env
```
```
source env/bin/activate
```
Установить зависимости из файла requirements.txt:
```
python3 -m pip install --upgrade pip
```
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
Примеры
Список доступных эндпоинтов:

api/v1/auth/signup/ - Авторизация
api/v1/auth/token/ - Получение JWT-токена
api/v1/categories/ -  Категории произведений
api/v1/genres/ - Жанры произведений.
api/v1/titles/ - Произведения, к которым пишут отзывы
api/v1/titles/{title_id}/reviews - Oтзывы на произведения
api/v1/titles/{title_id}/reviews/{review_id}/comments/ - Kомментарии к отзывам
api/v1/users/ - Пользователи проекта
api/v1/users/me/ - Личный профиль
