from django.test import TestCase
from django.test.client import RequestFactory
from django.urls import reverse

from flag_quest.views import CountriesMenuView


class CountriesMenuViewTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def test_countries_menu_view(self):
        request = self.factory.get(reverse("countries_menu"))
        response = CountriesMenuView.as_view()(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.template_name[0], "flag_quest/learning_list.html"
        )
        self.assertIn("continents", response.context_data)
