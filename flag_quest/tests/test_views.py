from django.test import Client, TestCase
from django.urls import reverse

from flag_quest.models import CountryInfo


class TestViews(TestCase):
    def setUp(self):
        self.client = Client()

    def test_index_view(self):
        response = self.client.get(reverse("index"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.template_name[0], "index.html")

    def test_results_view(self):
        response = self.client.get(reverse("results"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.template_name[0], "flag_quest/results.html")

    def test_about_view(self):
        response = self.client.get(reverse("about"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.template_name[0], "flag_quest/about.html")

    def test_details_view(self):
        self.country1 = CountryInfo.objects.create(
            name="test_country"
        )
        response = self.client.get(reverse("country_details",
                                           kwargs={"country": "test_country"}))
        self.assertEqual(response.status_code, 200)
