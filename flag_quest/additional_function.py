import random
from random import choice
from typing import Optional, Union

from django.core.exceptions import ObjectDoesNotExist
from django.db.models import QuerySet

from flag_quest.models import Answer, Continent, CountryInfo


def countries_generator(
    continent: Optional[str] = None,
) -> Union[QuerySet[CountryInfo], None]:
    all_countries = CountryInfo.objects.all()

    used_countries = Answer.objects.all().values_list("correct_answer", flat=True)
    filtered_countries = all_countries.exclude(name__in=used_countries)
    if continent and continent != "All Continents":
        continent_object = Continent.objects.get(name=continent)
    else:
        continent_object = choice(filtered_countries).continent_1_id
    return filtered_countries.filter(continent_1_id=continent_object).order_by("?")[:5]


def get_shuffled_list(input_list):
    return random.sample(input_list, len(input_list))


def question_set_generator(required_param, continent_name):
    countries = countries_generator(continent_name)

    if not countries:
        return None

    countries_item = get_country_attribute(countries[0], required_param)

    options = [(country.name, country.name) for country in countries]

    return {
        "countries_item": countries_item,
        "options": get_shuffled_list(options),
        "continent_name": continent_name,
        "correct_answer_country": get_country_attribute(countries[0], "name"),
        "correct_answer_additional_info": get_country_attribute(
            countries[0], "meaning_of_flag"
        ),
    }


def get_country_attribute(country, attr):
    attribute_mapping = {
        "flag": "flag_picture",
        "capital": "capital",
        "name": "name",
        "meaning_of_flag": "meaning_of_flag",
    }
    attribute = attribute_mapping.get(attr)
    return getattr(country, attribute, None) if attribute else None


def country_by_flag(flag_picture):
    try:
        return CountryInfo.objects.get(flag_picture=flag_picture).name
    except ObjectDoesNotExist:
        return "Country not found"


def total_result_calculator():
    answers = Answer.objects.all().count()
    correct_answers = Answer.objects.filter(is_correct=True).count()
    return [correct_answers, answers]


def get_country_info(country_name):
    try:
        return CountryInfo.objects.get(name=country_name)
    except CountryInfo.DoesNotExist:
        return "Country not found"
