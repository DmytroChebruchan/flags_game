import random
from random import choice

from django.core.exceptions import ObjectDoesNotExist

from flag_quest.forms import AnswerForm
from flag_quest.models import Answer, CountryInfo


def countries_generator(continent: str = None):
    all_countries = CountryInfo.objects.all()

    if continent:
        return all_countries.filter(continent=continent).order_by("?")[:5]

    random_continent = choice(all_countries).continent
    return all_countries.filter(continent=random_continent).order_by("?")[:5]


def get_shuffled_list(input_list):
    return random.sample(input_list, len(input_list))


def options_generator(question):
    return [(option[0], option[0]) for option in question["options"]]


def collect_correct_countries(flags):
    correct_countries = {}
    countries = CountryInfo.objects.all()
    for country in countries:
        if country.flag_picture in flags:
            correct_countries[country.flag_picture] = country.name
    return correct_countries


def context_generator(required_param, options_type):
    countries = countries_generator()

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


def country_by_flag(flag_picture):
    try:
        country = CountryInfo.objects.get(flag_picture=flag_picture)
        return country.name
    except ObjectDoesNotExist:
        return "Country not found"


def save_reply_of_user(returned_request):
    answer = Answer()
    answer.save_reply(returned_request)


def total_result_calculator():
    answers = Answer.objects.all().count()
    correct_answers = Answer.objects.filter(is_correct=True).count()
    result = (correct_answers, answers)
    return result
