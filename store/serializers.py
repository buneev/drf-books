from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from store.models import *


class BookSerializer(ModelSerializer):
    # данные поля не хранятся в бд, они будут вычисленны 'налету' через Annotate
    likes_count = serializers.SerializerMethodField()
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

