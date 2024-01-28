from django.http import Http404
from django.test import Client, TestCase
from django.urls import reverse

from flag_quest.models import CountryInfo
from flag_quest.views import CountryDetailsView


class TestViewsOnPing(TestCase):
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
        self.country1 = CountryInfo.objects.create(name="test_country")
        response = self.client.get(
            reverse("country_details", kwargs={"country": "test_country"})
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.template_name[0], "flag_quest/country_details.html"
        )


class TestDetailsView(TestCase):
    def setUp(self):
        self.client = Client()

    def test_get_object_not_found(self):
        view = CountryDetailsView()
        view.kwargs = {"country": "non_existing_country"}

        # Call the get_object method and expect Http404 exception
        with self.assertRaises(Http404):
            view.get_object()

    def test_get_object_success(self):
        view = CountryDetailsView()
        view.kwargs = {"country": "test_country"}

        # Simulate the existence of the country
        country = CountryInfo.objects.create(name="test_country")

        # Call the get_object method
        obj = view.get_object()

        # Check that the returned object matches the created country
        self.assertEqual(obj, country)
