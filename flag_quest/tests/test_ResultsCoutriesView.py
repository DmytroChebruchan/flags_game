import django
from django.test import Client, TestCase
from django.urls import reverse

from flag_quest.models import Answer
from flag_quest.tests.additional_functions import dummy_answers_creator

django.setup()


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
