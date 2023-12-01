import random
from random import choice
from flag_quest.models import CountryInfo, Answer
from django.core.exceptions import ObjectDoesNotExist


def correct_answer_generator(question: object) -> object:
    options = question['options']
    correct_answer = ''
    for option in options:
        if option[1] == 'correct':
            correct_answer = option[0]
            break

    return correct_answer

def countries_generator(continent: str = None):
    all_countries = CountryInfo.objects.all()

    if continent:
        return all_countries.filter(continent=continent).order_by("?")[:5]

    random_continent = choice(all_countries).continent
    return all_countries.filter(continent=random_continent).order_by("?")[:5]


def get_shuffled_list(input_list):
    return random.sample(input_list, len(input_list))


def options_generator(question):
    return [
        (option[0], option[0]) for option in question["options"]
    ]


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


def country_by_flag(flag_picture):
    try:
        country = CountryInfo.objects.get(flag_picture=flag_picture)
        return country.name
    except ObjectDoesNotExist:
        return "Country not found"  # Modify this message according to your requirements


def save_reply_of_user(returned_request):
    your_answer = returned_request['options_chosen']
    correct_answer = country_by_flag(returned_request['flag_picture'])

    answer = Answer(flag_picture=returned_request['flag_picture'],
                    your_answer=your_answer,
                    correct_answer=correct_answer,
                    is_correct=True if correct_answer == your_answer else False)
    answer.save()
