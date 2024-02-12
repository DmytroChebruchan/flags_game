from django.test import TestCase

from flag_quest.models import Answer, Continent, CountryInfo


class ContinentModelTest(TestCase):
    def test_continent_creation(self):
        continent = Continent.objects.create(
            name="Test Continent", description="Test Description"
        )
        self.assertEqual(continent.name, "Test Continent")
        self.assertEqual(continent.description, "Test Description")


class CountryInfoModelTest(TestCase):
    def setUp(self):
        self.continent = Continent.objects.create(name="Test Continent")

    def test_country_info_creation(self):
        country = CountryInfo.objects.create(
            name="Test Country",
            flag_picture="test.jpg",
            capital="Test Capital",
            continent_1=self.continent,
            meaning_of_flag="Test meaning of flag",
        )
        self.assertEqual(country.name, "Test Country")
        self.assertEqual(country.flag_picture, "test.jpg")
        self.assertEqual(country.capital, "Test Capital")
        self.assertEqual(country.continent_1, self.continent)
        self.assertEqual(country.meaning_of_flag, "Test meaning of flag")


class AnswerModelTest(TestCase):
    def setUp(self):
        self.continent = Continent.objects.create(name="Test Continent")
        self.country = CountryInfo.objects.create(
            name="Test Country",
            flag_picture="test.jpg",
            capital="Test Capital",
            continent_1=self.continent,
            meaning_of_flag="Test meaning of flag",
        )

    def test_answer_creation(self):
        answer = Answer.objects.create(
            flag_picture="test.jpg",
            is_correct=True,
            your_answer="Test Country",
            correct_answer="Test Country",
        )
        self.assertEqual(answer.flag_picture, "test.jpg")
        self.assertTrue(answer.is_correct)
        self.assertEqual(answer.your_answer, "Test Country")
        self.assertEqual(answer.correct_answer, "Test Country")

    def test_str_representation(self):
        # Create an instance of the Answer model
        answer = Answer(
            flag_picture="example_picture.png",
            is_correct=True,
            your_answer="Your answer",
            correct_answer="Correct answer"
        )

        # Check if the __str__ method returns the expected string
        expected_str = "Your answer"
        self.assertEqual(str(answer), expected_str)
