import random
from random import choice

from django.core.exceptions import ObjectDoesNotExist

from flag_quest.models import Answer, CountryInfo


def countries_generator(continent: str = None):
    all_countries = CountryInfo.objects.all()
    used_countries = Answer.objects.all().values_list("correct_answer", flat=True)
    filtered_countries = all_countries.exclude(name__in=used_countries)

    if continent:
        return filtered_countries.filter(continent=continent).order_by("?")[:5]

    random_continent = choice(filtered_countries).continent
    return filtered_countries.filter(continent=random_continent).order_by("?")[:5]


def get_shuffled_list(input_list):
    return random.sample(input_list, len(input_list))


def options_generator(question):
    if question:
        return [(option[0], option[0]) for option in question["options"]]
    return None


def adding_correct_answers(context):
    answers_context = context["object_list"]
    flags = [answer.flag_picture for answer in answers_context]

    correct_countries = collect_correct_countries(flags)

    correct_answers_handler(answers_context, correct_countries)


def correct_answers_handler(answers_context, correct_countries):
    total_correct_answers = 0
    for answer in answers_context:
        if answer.your_answer == correct_countries[answer.flag_picture]:
            answer.is_correct = True
            total_correct_answers = total_correct_answers + 1
        else:
            answer.correct_answer = correct_countries[answer.flag_picture]
        answer.save()


def collect_correct_countries(flags):
    correct_countries = {}
    countries = CountryInfo.objects.all()
    for country in countries:
        if country.flag_picture in flags:
            correct_countries[country.flag_picture] = country.name
    return correct_countries


def correct_answer_collector(question):
    if question is None:
        return None

    for answer in question["options"]:
        if answer[1] == "correct":
            return answer[0]

    return "no correct answer is detected"


def context_generator(required_param, options_type, continent):
    countries = countries_generator(continent)

    if not countries:
        return None

    country_question = countries.first()

    question = ""
    if required_param == "flag":
        question = country_question.flag_picture

    correct_answer = ""
    if options_type == "country":
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
        return "Country not found"


def save_reply_of_user(returned_request):
    # fix below
    try:
        your_answer = returned_request["selected_country"]
    except KeyError:
        your_answer = ""

    correct_answer = country_by_flag(returned_request["flag_picture"])

    answer = Answer(
        flag_picture=returned_request["flag_picture"],
        your_answer=your_answer,
        correct_answer=correct_answer,
        is_correct=True if correct_answer == your_answer else False,
    )
    answer.save()


def total_result_calculator():
    answers = Answer.objects.all().count()
    correct_answers = Answer.objects.filter(is_correct=True).count()
    result = (correct_answers, answers)
    return result


def get_country_info(country_name):
    try:
        country = CountryInfo.objects.get(name=country_name)
    except CountryInfo.DoesNotExist:
        return "Country not found"
    return country
