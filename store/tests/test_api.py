from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse

from store.models import Book
from store.serializers import BookSerializer


class BookApiTestCase(APITestCase):

    def test_get(self):

        book1 = Book.objects.create(name='Test book1', price='353.21')
        book2 = Book.objects.create(name='Test book2', price='763.75')

        url = reverse('book-list')
        # url = reverse('book-detail')
        response = self.client.get(url)
        serializer_data = BookSerializer([book1, book2], many=True).data

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data['results'])

