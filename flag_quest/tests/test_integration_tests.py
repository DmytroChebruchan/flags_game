import django
from django.test import TestCase

django.setup()
from flag_quest.additional_functions import total_result_calculator
from flag_quest.models import Answer


class TotalResultCalculatorTests(TestCase):
    def setUp(self):
        self.answer1 = Answer.objects.create(
            flag_picture="flag picture",
            is_correct=True,
            your_answer="your answer",
            correct_answer="your answer",
        )
        self.answer2 = Answer.objects.create(
            flag_picture="flag picture",
            is_correct=True,
            your_answer="your answer",
            correct_answer="your answer",
        )
        self.answer3 = Answer.objects.create(
            flag_picture="flag picture",
            is_correct=True,
            your_answer="your answer",
            correct_answer="your answer",
        )
        self.answer4 = Answer.objects.create(
            flag_picture="flag picture",
            is_correct=True,
            your_answer="your answer",
            correct_answer="your answer",
        )
        self.answer5 = Answer.objects.create(
            flag_picture="flag picture",
            is_correct=False,
            your_answer="your answer",
            correct_answer="correct answer",
        )

    def test_total_result_calculator(self):
        result = total_result_calculator()
        self.assertEqual([4, 5], result)
