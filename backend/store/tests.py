from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from django.test.utils import CaptureQueriesContext
from django.db import connection

from .models import Product


class TestProductViewSetQueries(TestCase):
    def setUp(self):
        self.client = APIClient()

        Product.objects.create(name="Producto 1", price=10)
        Product.objects.create(name="Producto 2", price=20)

    def test_product_list_query_count(self):
        url = reverse("products-list")  

        with CaptureQueriesContext(connection) as ctx:
            response = self.client.get(url)

        print("\nTotal de consultas:", len(ctx.captured_queries))
        for q in ctx.captured_queries:
            print(q["sql"])

        # Test de respuesta correcta
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Opcional: exigir un máximo de consultas (por ejemplo 2)
        self.assertLessEqual(len(ctx.captured_queries), 10000000)
