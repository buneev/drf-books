from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import ArticleView1, SingleArticleView, ArticleView4, ArticleViewSet

app_name = "article"

urlpatterns = [
    path('article/', ArticleView1.as_view()),
    path('article/<int:pk>', ArticleView1.as_view()),
    path('articles/', ArticleView4.as_view()),
    path('articles/<int:pk>', SingleArticleView.as_view()),
]

"""
DefaultRouter() позволяет значительно уменьшить код в URL.
Теперь если обратится по URL: http://127.0.0.1:8000/api/articles/ или 
http://127.0.0.1:8000/api/articles/1/  то опять все должно работать как раньше. 
"""

art_router = DefaultRouter()
art_router.register(r'arti', ArticleViewSet, basename='user')
urlpatterns += art_router.urls

