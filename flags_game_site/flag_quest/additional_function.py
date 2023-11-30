import random
from random import choice
from flag_quest.models import CountryInfo


def countries_generator(continent: str = None):
    all_countries = CountryInfo.objects.all()

    if continent:
        return all_countries.filter(continent=continent).order_by("?")[:5]

    random_continent = choice(all_countries).continent
    return all_countries.filter(continent=random_continent).order_by("?")[:5]


def get_shuffled_list(input_list):
    return random.sample(input_list, len(input_list))


def adding_correct_answers(context):
    answers_context = context["object_list"]
    flags = [answer.flag_picture for answer in answers_context]

    correct_countries = {}
    countries = CountryInfo.objects.all()
    for country in countries:
        if country.flag_picture in flags:
            correct_countries[country.flag_picture] = country.name

    total_correct_answers = 0
    for answer in answers_context:
        if answer.your_answer == correct_countries[answer.flag_picture]:
            answer.is_correct = True
            total_correct_answers = total_correct_answers + 1
        else:
            answer.correct_answer = correct_countries[answer.flag_picture]
        answer.save()


def context_generator(required_param, options_type):
    countries = countries_generator()

    if not countries:
        return None

    country_question = countries.first()

    if required_param == "flag":
        question = country_question.flag_picture

    if options_type is "country":
        correct_answer = country_question.name

    options = [(correct_answer, "correct")]
    options.extend((country.name, "wrong") for country in countries[1:])

    context = {"question": question, "options": get_shuffled_list(options)}
    return context
