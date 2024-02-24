from rest_framework import viewsets
from rest_framework.generics import get_object_or_404, GenericAPIView, CreateAPIView, ListAPIView, ListCreateAPIView, \
    RetrieveAPIView, RetrieveUpdateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.mixins import ListModelMixin, CreateModelMixin
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Article, Author
from .serializers import ArticleSerializer, ArticleSerializer2

"""
https://webdevblog.ru/sozdanie-django-api-ispolzuya-django-rest-framework-apiview/
https://webdevblog.ru/sozdanie-django-api-ispolzuya-djangorestframework-chast-2/
https://webdevblog.ru/sozdanie-django-api-ispolzuya-djangorestframework-chast-3/
"""


class ArticleView1(APIView):

    def get(self, request, pk=None):
        if pk:
            article = Article.objects.get(pk=pk)
            serializer = ArticleSerializer(article)
        else:
            articles = Article.objects.all()
            serializer = ArticleSerializer(articles, many=True)
        return Response(serializer.data)

    def post(self, request, pk=None):
        """
        [
            {
                "title": "test1",
                "description": "test1",
                "body": "test1"
            },
            {
                "title": "test2",
                "description": "test2",
                "body": "test2"
            }
        ]
        or
        {
            "title": "test1",
            "description": "test1",
            "body": "test1"
        }
        """

        if type(request.data) is dict:
            serializer = ArticleSerializer(data=request.data)
        elif type(request.data) is list:
            serializer = ArticleSerializer(data=request.data, many=True)

        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def put(self, request, pk):
        saved_article = get_object_or_404(Article.objects.all(), pk=pk)
        serializer = ArticleSerializer(instance=saved_article, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def delete(self, request, pk):
        article = get_object_or_404(Article.objects.all(), pk=pk)
        article.delete()
        return Response('deleted', status=204)


class ArticleView2(ListModelMixin, CreateModelMixin, GenericAPIView):
    """
    GenericAPIView отличается от APIView, тем что GenericAPIView
    расширяет возможности APIView, добавляя в него часто используемые
    методы list и detail. Сл-но в коде выше, этих двух моих костылей
    быть не должно, в статье их и нет.
    """
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer2

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def perform_create(self, serializer):
        author = get_object_or_404(Author, id=self.request.data.get('author_id'))
        return serializer.save(author=author)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class ArticleView3(ListAPIView, CreateAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer2

    def perform_create(self, serializer):
        author = get_object_or_404(Author, id=self.request.data.get('author_id'))
        return serializer.save(author=author)


class ArticleView4(ListCreateAPIView):
    """Вроде бы идеальная комбинация, но без множественного создания."""
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer2

    def perform_create(self, serializer):
        author = get_object_or_404(Author, id=self.request.data.get('author_id'))
        return serializer.save(author=author)

class SingleArticleView(RetrieveUpdateDestroyAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer2


class ArticleViewSet(viewsets.ModelViewSet):
    """То же самое что и выше, + на скриншоте api.png"""
    serializer_class = ArticleSerializer2
    queryset = Article.objects.all()

