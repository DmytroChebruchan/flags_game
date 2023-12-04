from django.test import TestCase, Client
from django.urls import reverse
from flag_quest.models import CountryInfo, Answer


class TestViews(TestCase):
    def setUp(self):
        self.client = Client()

    def test_index_view(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')

    def test_list_countries_view(self):
        response = self.client.get(reverse('list_of_countries'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'flag_quest/list_of_countries.html')
