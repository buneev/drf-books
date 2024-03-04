
https://www.youtube.com/playlist?list=PLyaCd9XYVI9DiMvYl-8OdZk7ktc6NQWrb
https://proproprogs.ru/django4 !!! Погружение в ORM Django
https://dzen.ru/a/ZUAAioxUhgegJTeo?share_to=link
https://ru.hexlet.io/courses/python-django-orm/lessons/annotation/theory_unit

## intro

#### postgresql локальный
sudo service postgresql start

#### Дать права пользователю на создание бд (для запуска тестов)
sudo -u postgres psql
ALTER USER books CREATEDB;

#### запуск тестов
python3 manage.py test .
python3 manage.py test store.tests.test_api

#### superusers
books / books
admin / 123456

#### shell - пример, доступа через my_book
python3 manage.py shell
> from django.contrib.auth.models import User
> 
> user = User.objects.get(id=2)
>
> user.my_books.all()
> 
> user.books.all()

## Celery

Запуск celery worker, который выполняет 2 задачи одновременно: 
>  python -m celery -A books worker -c 2 -l info

Получение текущего состояния воркера
> python3 -m celery -A books inspect active
>
> python3 -m celery -A books inspect stats

## Flower
Запуск flower http://0.0.0.0:5555:
> celery -A books flower 

## s3 timeweb

https://timeweb.cloud/my/storage

