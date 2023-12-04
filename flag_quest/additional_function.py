import random
from random import choice

from django.core.exceptions import ObjectDoesNotExist

from flag_quest.forms import AnswerForm
from flag_quest.models import Answer, CountryInfo


def countries_generator(required_continent: str = None):
    all_countries = CountryInfo.objects.all()

    if required_continent:
        return all_countries.filter(continent=required_continent).order_by("?")[
               :5]

    random_continent = choice(all_countries).continent
    return all_countries.filter(continent=random_continent).order_by("?")[:5]


def get_shuffled_list(input_list):
    return random.sample(input_list, len(input_list))


def options_generator(question):
    return [(option[0], option[0]) for option in question["options"]]


def context_generator(required_param, options_type, continent):
    countries = countries_generator(continent)

    if not countries:
        return None

    country_question = countries.first()

    if required_param == "flag":
        question = country_question.flag_picture

    if options_type == "country":
        correct_answer = country_question.name

    options = [(correct_answer, "correct")]
    options.extend((country.name, "wrong") for country in countries[1:])
    # options.append(('I do not know', "idk"))

    context = {"question": question, "options": get_shuffled_list(options)}
    return context


def save_reply_of_user(returned_request):
    answer = Answer()
    answer.save_reply(returned_request)


def total_result_calculator():
    answers = Answer.objects.all().count()
    correct_answers = Answer.objects.filter(is_correct=True).count()
    result = (correct_answers, answers)
    return result
