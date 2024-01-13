from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Article
from .serializers import ArticleSerializer


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


