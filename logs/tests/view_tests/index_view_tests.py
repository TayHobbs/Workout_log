from django.test import TestCase
from django.test.client import Client
from django.core.urlresolvers import reverse


class IndexViewTests(TestCase):

    def test_index_view(self):
        response = Client().get(reverse("index"))
        self.assertEqual(response.status_code, 200)
