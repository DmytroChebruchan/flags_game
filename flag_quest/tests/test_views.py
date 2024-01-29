from unittest.mock import patch

from django.http import Http404
from django.test import Client, TestCase
from django.urls import reverse

from flag_quest.forms import AnswerForm
from flag_quest.models import Answer, Continent, CountryInfo
from flag_quest.tests.additional_functions import dummy_answers_creator
from flag_quest.views import CountryDetailsView, GamePage
import django

django.setup()


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
        self.assertEqual(len(response.context_data["results"]), 2)

    def test_few_pages_results_countries_get(self):
        dummy_answers_creator(10)
        response = self.client.get(reverse("results"))
        self.assertEqual(len(response.context_data["results"]), 5)

    def test_results_countries_post(self):
        # Create sample answer objects
        Answer.objects.create(
            flag_picture="test_flag_picture_1",
            is_correct=True,
            your_answer="correct_answer_1",
            correct_answer="correct_answer_1",
        )
        Answer.objects.create(
            flag_picture="test_flag_picture_2",
            is_correct=False,
            your_answer="incorrect_answer_2",
            correct_answer="correct_answer_2",
        )

        # Make POST request to clean answers
        response = self.client.post(reverse("results"), {"clean": "clean"})

        # Check redirection
        self.assertRedirects(response, reverse("results"))

        # Check if all Answer objects are deleted
        self.assertEqual(Answer.objects.count(), 0)


class TestGamePage(TestCase):
    def setUp(self):
        self.continent = Continent.objects.create(name="Test Continent")
        self.country = CountryInfo.objects.create(
            name="Test Country",
            flag_picture="test_flag.png",
            continent_1=self.continent,
            meaning_of_flag="Test meaning of flag",
        )
        self.country_1 = CountryInfo.objects.create(
            name="Test Country 2",
            flag_picture="test_flag.png",
            continent_1=self.continent,
            meaning_of_flag="Test meaning of flag",
        )

        self.answer = Answer.objects.create(
            flag_picture="test_flag.png",
            is_correct=True,
            your_answer="Test Country",
            correct_answer="Test Country",
        )

    def test_game_page_loads_successfully(self):
        response = self.client.get(reverse("game"))
        self.assertEqual(response.status_code, 200)

    def test_correct_template_used(self):
        response = self.client.get(reverse("game"))
        self.assertEqual(
            response.template_name[0], "flag_quest/flag_quest.html"
        )

    def test_get_context_data(self):
        view = GamePage()
        view.kwargs = {"continent_name": "Test Continent"}
        context = view.get_context_data()

        self.assertIn("question_set", context)
        self.assertEqual(
            context["question_set"]["continent_name"], "Test Continent"
        )
        self.assertIn("form", context)

    @patch("flag_quest.models.CountryInfo.objects.get")
    def test_form_valid(self, mock_get_country_info):
        # Mock CountryInfo object
        country_info = CountryInfo(
            name="Test Country", flag_picture="test_flag.jpg"
        )
        mock_get_country_info.return_value = country_info

        # Create a mock question set with options and country item
        question_set = {
            "options": [("Test Country", "Test Country")],
            # Update the option format
            "countries_item": "Test Country",  # Update the country item format
        }

        # Initialize form and set parameters
        form = AnswerForm()
        form.set_params(question_set, add_flag=True)

        # Bind the form
        form.is_bound = True
        form.data = {
            "your_answer": "Test Country",  # Update the answer format
            "flag_picture": "test_flag.jpg",
        }

        # Create a mock request with required kwargs
        kwargs = {"continent_name": "TestContinent"}
        request = self.client.post(reverse("game"), kwargs=kwargs)

        # Set up the view
        view = GamePage()
        view.request = request
        view.kwargs = kwargs

        # Test the form_valid method
        response = view.form_valid(form)

        # Assert that the response is a redirect
        self.assertTrue(response.url.startswith(reverse("game")))
        self.assertEqual(response.status_code, 302)

        # Assert that the answer is saved
        self.assertTrue(Answer.objects.exists())
        saved_answer = Answer.objects.first()
        self.assertEqual(saved_answer.correct_answer, country_info.name)
        self.assertTrue(saved_answer.is_correct)


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
        self.assertIn("flag_quest/list_of_countries.html",
                      response.template_name)

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
