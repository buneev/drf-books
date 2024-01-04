from django.test import TestCase

from store.models import Book
from store.serializers import BookSerializer


class BookSerializerTestCase(TestCase):

    def setUp(self):
        self.book1 = Book.objects.create(name='Test book1', price=353.21)
        self.book2 = Book.objects.create(name='Test book2', price=763.75)


    def test_ok(self):
        data = BookSerializer([self.book1, self.book2], many=True).data
        expected_data = [
            {
                'id': self.book1.id,
                'name': 'Test book1',
                'price': 353.21,
            },
            {
                'id': self.book2.id,
                'name': 'Test book2',
                'price': 763.75,
            },
        ]
        self.assertEqual(expected_data, data)