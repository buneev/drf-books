from rest_framework import serializers
from .models import Article


class ArticleSerializer(serializers.Serializer):

    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(max_length=120)
    description = serializers.CharField()
    body = serializers.CharField()
    author_id = serializers.IntegerField(required=False)

    def create(self, validated_data):
        return Article.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get('description', instance.description)
        instance.body = validated_data.get('body', instance.body)
        instance.author_id = validated_data.get('author_id', instance.author_id)
        instance.save()
        return instance


class ArticleSerializer2(serializers.ModelSerializer):
    """
    Используя ModelSerializer, мы сразу получаем методы
    create и update. А так же набор валидаторов по умолчанию.
    """

    class Meta:
        model = Article
        fields = ('id', 'title', 'description', 'body', 'author_id')

