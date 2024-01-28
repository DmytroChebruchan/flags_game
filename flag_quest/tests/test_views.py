from django.http import Http404
from django.test import Client, TestCase
from django.urls import reverse

from flag_quest.forms import AnswerForm
from flag_quest.models import CountryInfo, Answer
from flag_quest.tests.additional_functions import dummy_answers_creator
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


class TestResultsCountriesView(TestCase):
    def setUp(self):
        self.client = Client()

    def test_one_page_results_countries_get(self):
        dummy_answers_creator(2)
        response = self.client.get(reverse("results"))
        self.assertTrue("results" in response.context_data)
        self.assertEqual(len(response.context_data["results"]),
                         2)

    def test_few_pages_results_countries_get(self):
        dummy_answers_creator(10)
        response = self.client.get(reverse("results"))
        self.assertEqual(len(response.context_data["results"]),
                         5)

    def test_results_countries_post(self):
        # Create sample answer objects
        Answer.objects.create(
            flag_picture="test_flag_picture_1",
            is_correct=True,
            your_answer="correct_answer_1",
            correct_answer="correct_answer_1"
        )
        Answer.objects.create(
            flag_picture="test_flag_picture_2",
            is_correct=False,
            your_answer="incorrect_answer_2",
            correct_answer="correct_answer_2"
        )

        # Make POST request to clean answers
        response = self.client.post(reverse("results"), {"clean": "clean"})

        # Check redirection
        self.assertRedirects(response, reverse("results"))

        # Check if all Answer objects are deleted
        self.assertEqual(Answer.objects.count(), 0)


class TestGamePage(TestCase):
    def test_game_page_loads_successfully(self):
        response = self.client.get(reverse("game"))
        self.assertEqual(response.status_code, 200)

    def test_correct_template_used(self):
        response = self.client.get(reverse("game"))
        self.assertEqual(response.template_name[0],
                         "flag_quest/flag_quest.html")

    def test_context_data(self):
        continent_name = "Europe"

        response = self.client.get(
            reverse("game", kwargs={"continent_name": continent_name}))

        # Check if the correct context data is present
        self.assertIn("form", response.context_data)
        self.assertIsInstance(response.context_data["question_set"], dict)
