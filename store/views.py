from random import randint
from django.db.models import Count, Case, When, Avg, Max, Min, Sum, Q
from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import mixins, permissions, status
from rest_framework.decorators import api_view, permission_classes, action
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
    """Представление на основе функции."""

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

    def get(self, request, min: int, max: int):
        """Пример передачи параметров."""

        resp = {
            'random_number': randint(min, max),
            'url': 'https://dzen.ru/a/ZUAAioxUhgegJTeo?share_to=link',
            'info': "Как правило, имеет смысл использовать APIView класс,"
                    "когда конечная точка вашего API не выполняет операции "
                    "CRUD над моделями баз данных.",
        }
        return Response(resp)

    def post(self, request):
        number = randint(request.data.get('min', 1), request.data.get('max', 100))
        return Response({'random_number': number})


class UserRegistrationView(APIView):
    """
    body example:
    {
        "username": "admin",
        "password": ""
        -- "phone": "1234"
    }
    """
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        serializer = UserSerializers(instance=request.user)
        return Response(serializer.data)

    def post(self, request):
        serializer = UserSerializers(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save() # вызывает метод create в сериализаторе
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class BookView(ModelViewSet):
    """
    @price_info - получение sum/avg/min/max цены среди всех книг магазина;
    @likes_cnt - количество всех лайков;
    @q - пример работы ORM-команды с классом Q;
    """

    # для каждой книги считаем кол-во лайков и рейтинг
    queryset = Book.objects.all().annotate(
        annotated_likes_count=Count(Case(When(userbookrelation__like=True, then=1))),
        rating=Avg('userbookrelation__rate')
    ).select_related('owner').prefetch_related('readers').order_by('id')
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

    # TODO://
    # @action(detail=True, methods=['put'])
    # def upload_file(self, request: drf_request, pk: int):
    #     """Загрузка файлов."""

    @action(detail=False, methods=['get'])
    def price_info(self, request):
        """
        Aggregate.
        Получение sum/avg/min/max цены среди всех книг магазина
        """

        # bad example:
        # total_price = sum(book.price for book in Book.objects.all())
        # ORM честно запросит все книги из базы и поместит данные каждой
        # книги в объект класса Book. А затем в коде потребуется только цена — это
        # уже выглядит как лишняя работа! Django ORM умеет запрашивать только часть данных.

        # good example
        price_info = Book.objects.aggregate(
            sum_books_price=Sum('price'), avg_books_price=Avg('price'),
            min_price=Min('price'), max_price=Max('price')
        )

        # Как можно заметить, каждый запрос на агрегацию возвращает
        # не сами книги, а только итоговый результат.
        return Response(price_info)

    @action(detail=False, methods=['get', 'post'])
    def likes_cnt(self, request):
        """
        Annotate.
        Каждый объект будет иметь дополнительные атрибуты. Каждый атрибут будет
        хранить результат соответствующей агрегации относительно текущего объекта.
        .aggregate(Count('postcomment')) - подсчитает количество всех комментариев, а
        .annotate(Count('postcomment')) - даст количество комментариев к каждому посту.
        https://ru.hexlet.io/courses/python-django-orm/lessons/annotation/theory_unit
        """

        # =)))
        data = Book.objects.annotate(
            likes_count=Count(Case(When(userbookrelation__like=True, then=1))),
        ).aggregate(likes_count_by_all_book_hard=Sum('likes_count'))

        data['likes_count_by_all_book_eazy'] = UserBookRelation.objects.filter(like=True).count()
        return Response(data)

    @action(detail=False, methods=['get'])
    def q(self, request):
        """
        Q. Если в условии нужно использовать логическое ИЛИ, а также НЕ,
        то вместо перечисления критериев отбора через запятую, следует
        использовать специальный класс Q.
        https://proproprogs.ru/django4/django4-orm-komandy-s-klassom-q
        https://metanit.com/python/django/5.13.php # gt, gte, lte, lt
        """

        queryset = Book.objects.filter(
            Q(id__in=[1, 2]) | Q(price__gt=400), name__icontains="Boo"
        )
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class UserBookRelationView(
    mixins.UpdateModelMixin,
    GenericViewSet
):
    queryset = UserBookRelation.objects.all()
    serializer_class = UserBookRelationSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'book'

    # lookup_field - в данном примере, основная идея в том,
    # чтобы менять записи в базе не по id связи (книг и действий пользователей),
    # а по id книги и пользователя; 23 в запросе /api/user_book_relation/23/ это
    # не id связи (объекта) как обычно, 23 - это id книги.

    # lookup_field - иногда нам может потребоваться выполнить поиск экземпляра
    # по полю, отличному от pk. Для этого мы должны установить lookup_field
    # свойство в нашем классе view. Также потребуется изменить имя параметра
    # при регистрации маршрута.

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

