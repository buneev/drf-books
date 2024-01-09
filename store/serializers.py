from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from store.models import *

"""
Сериализаторы в DRF отвечают за следующее:
1. Преобразование экземпляров модели и наборов запросов в собственные типы данных Python.
2. Проверка данных, предоставленных пользователем.
3. Создание и обновление экземпляров моделей баз данны
"""


class BookSerializer(ModelSerializer):
    likes_count = serializers.SerializerMethodField()
    # данные поля не хранятся в бд, они будут вычисленны 'налету' через Annotate
    annotated_likes_count = serializers.IntegerField(read_only=True)
    rating = serializers.DecimalField(max_digits=3, decimal_places=2, read_only=True)

    class Meta:
        model = Book
        fields = (
            'id', 'name', 'description', 'price', 'author_name',
            'owner', 'likes_count', 'annotated_likes_count', 'rating'
        )

        extra_kwargs = {
            # read_only так как иначе можно будет выбирать пользователя при создании книги
            'owner': {'read_only': True},
        }

    def get_likes_count(self, instance):
        return UserBookRelation.objects.filter(book=instance, like=True).count()


class UserBookRelationSerializer(ModelSerializer):
    class Meta:
        model = UserBookRelation
        fields = '__all__'

