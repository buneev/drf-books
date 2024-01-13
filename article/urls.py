from django.urls import path
from .views import ArticleView1

app_name = "article"

urlpatterns = [
    path('v1/article/', ArticleView1.as_view()),
    path('v1/article/<int:pk>', ArticleView1.as_view())
]

