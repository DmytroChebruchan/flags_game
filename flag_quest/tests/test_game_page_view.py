from unittest.mock import patch

import django
from django.test import TestCase
from django.urls import reverse

from flag_quest.constants import CONTINENTS
from flag_quest.forms import AnswerForm
from flag_quest.models import Answer, Continent, CountryInfo
from flag_quest.views import GameMenuView, GamePage

django.setup()


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

    def test_get_context_data_method(self):
        view = GameMenuView()
        context = view.get_context_data()

        self.assertIn("continents", context)
        self.assertEqual(context["continents"], CONTINENTS)
