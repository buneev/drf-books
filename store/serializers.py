from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from store.models import *

"""
Сериализаторы в DRF отвечают за следующее:
1. Преобразование экземпляров модели и наборов запросов в собственные типы данных Python.
2. Проверка данных, предоставленных пользователем.
3. Создание и обновление экземпляров моделей баз данны
"""


def phone_validate_func(phone_number: str):
    """Проверка для каждого поля выполняется Field классами."""

    if len(phone_number) < 6:
        raise serializers.ValidationError(
            'Длина телефона должна быть >= 6 симмволов'
        )

class BookReaderSerialiser(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('first_name', 'last_name')


class BookSerializer(ModelSerializer):

    # this is a read-only field
    # likes_count = serializers.SerializerMethodField()

    # поля annotated_likes_count и rating не хранятся в бд, они будут вычислены 'налету' через Annotate
    annotated_likes_count = serializers.IntegerField(read_only=True)
    rating = serializers.DecimalField(max_digits=3, decimal_places=2, read_only=True)
    # с помощью source указываем откуда получить имя, p.s.: owner = models.ForeignKey()
    owner_name = serializers.CharField(source='owner.username', default='', read_only=True)
    readers = BookReaderSerialiser(many=True)
    # если хотим изменить имя поля
    # readers_abc = BookReaderSerialiser(many=True, source='readers')

    class Meta:
        model = Book
        fields = (
            'id', 'name', 'description', 'price', 'author_name',
            'owner', 'annotated_likes_count', 'rating',
            # 'likes_count',
            'owner_name', 'readers',
        )

        extra_kwargs = {
            # read_only так как иначе можно будет выбирать пользователя при создании книги
            'owner': {
                'read_only': True,
                'required': True,
            },
        }

    # def get_likes_count(self, instance):
    #     """Делается много запросов. Есть реализация через annotate (поле annotated_likes_count)."""
    #     return UserBookRelation.objects.filter(book=instance, like=True).count()


class UserBookRelationSerializer(ModelSerializer):
    class Meta:
        model = UserBookRelation
        fields = '__all__'


class UserSerializers(serializers.Serializer):
    email = serializers.EmailField(required=False)
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)
    # phone = serializers.CharField(validators=[phone_validate_func])

    def validate_username(self, value):
        """
        Проверка для каждого поля, выполняемая Serializer классом.
        В некоторых ситуациях вам может потребоваться проверка для
        конкретного поля только на одной из ваших конечных точек.
        """

        if not value:
            return value
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError(
                'Пользователь с таким username уже существует'
            )
        return value

    def validate(self, attrs):
        """Проверить несколько полей одновременно! """

        email = attrs.get('email')
        username = attrs.get('username')
        return attrs

    def create(self, validated_data):
        """Этот метод будет запущен, если проверка прошла успешно."""

        return User.objects.create(**validated_data)

