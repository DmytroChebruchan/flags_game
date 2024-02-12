import django
from django.http import Http404
from django.test import Client, TestCase

from flag_quest.models import CountryInfo
from flag_quest.views import CountryDetailsView

django.setup()


class TestDetailsView(TestCase):
    def setUp(self):
        self.client = Client()
        self.view = CountryDetailsView()

    def test_get_object_not_found(self):
        self.view.kwargs = {"country": "non_existing_country"}

        # Call the get_object method and expect Http404 exception
        with self.assertRaises(Http404):
            self.view.get_object()

    def test_get_object_success(self):
        self.view.kwargs = {"country": "test_country"}

        # Simulate the existence of the country
        country = CountryInfo.objects.create(name="test_country")

        # Call the get_object method
        obj = self.view.get_object()

        # Check that the returned object matches the created country
        self.assertEqual(obj, country)
