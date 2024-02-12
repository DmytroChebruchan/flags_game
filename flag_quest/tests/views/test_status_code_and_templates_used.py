import django
from django.test import Client, TestCase
from django.urls import reverse

from flag_quest.models import CountryInfo

django.setup()


class TestViewsStatusCode(TestCase):
    def setUp(self):
        self.client = Client()

    def test_index_view(self):
        response = self.client.get(reverse("index"))
        self.assertEqual(response.status_code, 200)

    def test_results_view(self):
        response = self.client.get(reverse("results"))
        self.assertEqual(response.status_code, 200)

    def test_about_view(self):
        response = self.client.get(reverse("about"))
        self.assertEqual(response.status_code, 200)

    def test_details_view(self):
        self.country1 = CountryInfo.objects.create(name="test_country")
        response = self.client.get(
            reverse("country_details", kwargs={"country": "test_country"})
        )
        self.assertEqual(response.status_code, 200)


class TestViewsTemplates(TestCase):
    def setUp(self):
        self.client = Client()

    def test_index_template(self):
        response = self.client.get(reverse("index"))
        self.assertEqual(response.template_name[0], "index.html")

    def test_results_template(self):
        response = self.client.get(reverse("results"))
        self.assertEqual(response.template_name[0], "flag_quest/results.html")

    def test_about_template(self):
        response = self.client.get(reverse("about"))
        self.assertEqual(response.template_name[0], "flag_quest/about.html")

    def test_details_template(self):
        self.country1 = CountryInfo.objects.create(name="test_country")
        response = self.client.get(
            reverse("country_details", kwargs={"country": "test_country"})
        )
        self.assertEqual(
            response.template_name[0], "flag_quest/country_details.html"
        )
