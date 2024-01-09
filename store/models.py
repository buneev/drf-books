from django.contrib.auth.models import User
from django.db import models

"""
# Связь ManyToManyField (through, related_name)
https://metanit.com/python/django/5.7.php
https://www.youtube.com/watch?v=_vj9rh36UOA (09:10)
"""

RATE_CHOICES = (
    (1, 'Bad'),
    (2, 'Ok'),
    (3, 'Good'),
    (4, 'Amazing')
)

class Book(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField('Описание', null=True, max_length=255)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    author_name = models.CharField(max_length=255, null=True, default=None)
    # если user удалится, оставляем созданные им книги (избранное, можно было бы и удалить)
    owner = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        # user = User.objects.get(id=2)
        # user.my_books.all()
        related_name='my_books', # default related_name: 'book_set'
    )
    readers = models.ManyToManyField(
        User,
        # связь ManyToMany реализовали через кастомную таблицу UserBookRelation, для добавления своих полей,
        # без явного создания таблицы UserBookRelation, она была бы создана, но без доп. полей
        through='UserBookRelation',
        # user = User.objects.get(id=2)
        # user.books.all()
        related_name='books', # default related_name: 'book_set'
    )

    def __str__(self):
        return f'Id {self.id}: {self.name}'


class UserBookRelation(models.Model):
    # если пользователя удалят, удаляем лайки пользователя
    # если книгу удалят, удаляем её лайки и рейтинг
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    like = models.BooleanField(default=False)
    in_bookmarks = models.BooleanField(default=False)
    rate = models.PositiveSmallIntegerField(choices=RATE_CHOICES, null=True)

    def __str__(self):
        return f'{self.user.username}: {self.book.name}, RATE {self.rate}'

