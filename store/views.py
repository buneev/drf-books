from random import randint

from django.db.models import Count, Case, When, Avg
from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import mixins, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.filters import SearchFilter, OrderingFilter

from store.filters import BookFilter
from store.models import Book, UserBookRelation
from store.permissions import IsOwnerOrAdminOrReadOnly
from store.serializers import *


@api_view(['GET', 'POST'])
@permission_classes([permissions.AllowAny])
def get_random_number(request):

    if request.method == 'GET':
        number = randint(1, 100)
    elif request.method == 'POST':
        number = randint(
            request.data.get('min', 1),
            request.data.get('max', 100)
        )

    resp = {
        'random_number': number,
        'info': 'Представления в DRF могут быть созданы как на основе классов, '
                'так и функций. Для простых эндпойнтов чаще используются функции.',
    }
    return Response(resp)


class RandomNumberView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, min, max):
        resp = {
            'random_number': randint(min, max),
            'url': 'https://dzen.ru/a/ZUAAioxUhgegJTeo?share_to=link',
            'info': "Когда имеет смысл использовать APIView класс? "
                    "Как правило, когда конечная точка вашего API не "
                    "выполняет операции CRUD (создание, чтение, "
                    "обновление, удаление) над моделями баз данных.",
        }
        return Response(resp)

    def post(self, request):
        number = randint(request.data.get('min', 1), request.data.get('max', 100))
        return Response({'random_number': number})


class BookView(ModelViewSet):
    queryset = Book.objects.all().annotate(
        annotated_likes_count=Count(Case(When(userbookrelation__like=True, then=1))),
        rating=Avg('userbookrelation__rate')
    )
    serializer_class = BookSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = BookFilter
    # filterset_fields = ['name', 'price']
    search_fields = ['name', 'price'] # ищем сразу в разных полях
    ordering_fields = ['id', 'name', 'price']
    permission_classes = [IsOwnerOrAdminOrReadOnly]

    def perform_create(self, serializer):
        serializer.validated_data['owner'] = self.request.user
        serializer.save()


class UserBookRelationView(
    mixins.UpdateModelMixin,
    GenericViewSet
):
    queryset = UserBookRelation.objects.all()
    serializer_class = UserBookRelationSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'book'

    # lookup_field - тут основная идея в том,
    # чтобы менять записи в базе не по id связи (книг и действий пользователей),
    # а по id книги и пользователя; 23 в запросе /api/user_book_relation/23/ это
    # не id связи (объекта) как обычно, 23 - это id книги

    def get_object(self):
        # put/patch запрос
        # создаем, либо находим связь книги и пользователя.
        # если нашли связь, то меняем рейтинг и/или лайк; если не нашли, то
        # создаем связь т.е. устанавливаем рейтинг и/или лайк.

        obj, _ = UserBookRelation.objects.get_or_create(
            user=self.request.user,
            book_id=self.kwargs['book']
        )
        return obj

