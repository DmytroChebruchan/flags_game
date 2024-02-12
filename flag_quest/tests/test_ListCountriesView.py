import django
from django.test import TestCase
from django.urls import reverse

from flag_quest.models import Continent, CountryInfo

django.setup()


class ListCountriesViewTest(TestCase):
    def setUp(self):
        self.continent = Continent.objects.create(
            name="Test Continent", description="Test description"
        )
        self.continent2 = Continent.objects.create(
            name="Test Continent 2", description="Test descr 2"
        )
        self.country = CountryInfo.objects.create(
            name="Test Country", continent=self.continent
        )
        self.country1 = CountryInfo.objects.create(
            name="Test Country 1", continent=self.continent
        )
        self.country2 = CountryInfo.objects.create(
            name="Test Country 2", continent=self.continent2
        )
        self.country3 = CountryInfo.objects.create(
            name="Test Country 3", continent=self.continent2
        )

    def test_view_returns_correct_template(self):
        response = self.client.get(reverse("all_countries"))
        self.assertEqual(response.status_code, 200)
        self.assertIn(
            "flag_quest/list_of_countries.html", response.template_name
        )

    def test_view_context_contains_expected_data(self):
        response = self.client.get(reverse("all_countries"))
        self.assertIn("countries", response.context_data)
        self.assertIn("continent", response.context_data)

    def test_queryset_filtering_by_continent(self):
        context_data = self.client.get(
            reverse(
                "countries_by_continent",
                kwargs={"continent": self.continent.name},
            )
        ).context_data
        self.assertEqual("Test Continent", context_data["continent"])
        self.assertEqual(
            "Test description", context_data["continent_description"]
        )
