from django.test import TestCase
from unittest.mock import patch

from flag_quest.models import Answer, Continent, CountryInfo
from flag_quest.additional_functions import (QuestionSet,
                                             total_result_calculator,
                                             add_numbers_to_countries)

from unittest.mock import patch


class QuestionSetTests(TestCase):
    def setUp(self):
        # Create necessary objects for testing
        continent = Continent.objects.create(name="Test Continent")
        self.country1 = CountryInfo.objects.create(name="Country1",
                                                   continent_1=continent,
                                                   flag_picture='link_to_flag',
                                                   meaning_of_flag='meaning')
        self.country2 = CountryInfo.objects.create(name="Country2",
                                                   continent_1=continent)
        self.country3 = CountryInfo.objects.create(name="Country3",
                                                   continent_1=continent)
        self.country4 = CountryInfo.objects.create(name="Country4",
                                                   continent_1=continent)
        self.country5 = CountryInfo.objects.create(name="Country5",
                                                   continent_1=continent)

    def test_flag_adding(self):
        question_set = QuestionSet(continent_name="Test Continent",
                                   set_flag=True)
        country_names = [country.name for country in question_set.countries]
        expected_names = ["Country1", "Country2", "Country3", "Country4",
                          "Country5"]
        self.assertEqual(country_names, expected_names)
        self.assertEqual(question_set.continent_name, "Test Continent")
        self.assertEqual(question_set.correct_answer_additional_info, 'meaning')
        self.assertEqual(question_set.countries_item, 'link_to_flag')
        self.assertEqual(question_set.country.name, "Country1")

    def test_dict_context(self):
        question_set = QuestionSet(continent_name="Test Continent",
                                   set_flag=True)
        context = question_set.dict_context()

        self.assertIn('countries_item', context)
        self.assertIn('options', context)
        self.assertIn('continent_name', context)
        self.assertIn('correct_answer_country', context)
        self.assertIn('correct_answer_additional_info', context)

    def test_countries_setter_with_continent_name(self):
        question_set = QuestionSet(continent_name="Test Continent")
        self.assertEqual(len(question_set.countries), 5)

    def test_countries_setter_without_continent_name(self):
        with patch('flag_quest.additional_functions.choice') as mock_choice:
            mock_choice.return_value = self.country1
            question_set = QuestionSet()
            self.assertEqual(len(question_set.countries), 5)

    def test_flag_setter(self):
        question_set = QuestionSet(set_flag=True)
        self.assertEqual(question_set.countries_item,
                         self.country1.flag_picture)
        self.assertEqual(question_set.correct_answer_additional_info,
                         self.country1.meaning_of_flag)

    def test_options_setter(self):
        question_set = QuestionSet(continent_name="Test Continent",
                                   set_flag=True)
        # Extract country names from CountryInfo objects
        country_names = set([country.name for country in
                             question_set.countries])

        # Compare extracted country names with options
        self.assertEqual(len(question_set.options), 5)
        self.assertEqual(country_names,
                         set([option[0] for option in question_set.options]))

# class TotalResultCalculatorTests(TestCase):
#     def test_total_result_calculator(self):
#         # Create some Answer objects for testing
#         Answer.objects.create(is_correct=True)
#         Answer.objects.create(is_correct=False)
#         Answer.objects.create(is_correct=True)
#
#         result = total_result_calculator()
#         self.assertEqual(result, [2, 3])
#
#
# class AddNumbersToCountriesTests(TestCase):
#     def test_add_numbers_to_countries(self):
#         # Create a mock context for testing
#         context = {'page_obj': {'number': 2}}
#         el_name = 'your_element_name'
#         paginate_by = 10
#
#         add_numbers_to_countries(paginate_by, context, el_name)
#
#         # Check if the counter attribute is added to each country in the context
#         self.assertEqual(context[el_name][0].counter, 11)
#         self.assertEqual(context[el_name][1].counter, 12)
