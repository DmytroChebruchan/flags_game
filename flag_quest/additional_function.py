import random
from random import choice
from typing import Optional, Union, List, Tuple

from django.core.exceptions import ObjectDoesNotExist
from django.db.models import QuerySet

from flag_quest.models import Answer, Continent, CountryInfo


def countries_generator(
        continent: Optional[str] = None,
) -> Union[QuerySet[CountryInfo], None]:
    all_countries = CountryInfo.objects.all()

    used_countries = Answer.objects.all().values_list("correct_answer",
                                                      flat=True)
    filtered_countries = all_countries.exclude(name__in=used_countries)
    if continent and continent != "All Continents":
        continent_object = Continent.objects.get(name=continent)
    else:
        continent_object = choice(filtered_countries).continent_1_id
    return filtered_countries.filter(continent_1_id=continent_object).order_by(
        "?")[:5]


def get_shuffled_list(input_list):
    return random.sample(input_list, len(input_list))


def avail_countries_generator():
    all_countries = CountryInfo.objects.all()
    used_countries = Answer.objects.all().values_list("correct_answer",
                                                      flat=True)
    return all_countries.exclude(name__in=used_countries)


def continent_getter(continent_name, filtered_countries):
    if continent_name and continent_name != "All Continents":
        continent_object = Continent.objects.get(name=continent_name)
    else:
        continent_object = choice(filtered_countries).continent_1_id
    return continent_object


class QuestionSet():
    countries: QuerySet[CountryInfo]
    country: CountryInfo
    correct_answer_additional_info: str
    continent_name: str
    options: List[Tuple[str, str]]
    countries_item: str

    def __init__(self, continent_name: Optional[str] = None):
        self.continent_name = continent_name
        self.countries = countries_generator(continent_name)
        self.country = self.countries.first()
        self.options_setter()

    def countries_setter(self, continent_name: Optional[str] = None):
        # sorting out used flags
        filtered_countries = avail_countries_generator()

        # gets continent object
        continent_object = continent_getter(continent_name, filtered_countries)

        # selecting random countries on continent
        self.countries = filtered_countries.filter(
            continent_1_id=continent_object).order_by(
            "?")[:5]

    def flag_setter(self):
        self.countries_item = self.country.flag_picture
        self.additional_info_generator('meaning_of_flag')

    def additional_info_generator(self, requirement: str):
        if requirement == 'meaning_of_flag':
            self.correct_answer_additional_info = self.country.meaning_of_flag

    def options_setter(self):
        options = [(country.name, country.name) for country in self.countries]
        self.options = get_shuffled_list(options)

    def dict_context(self):
        return {
            "countries_item": self.countries_item,
            "options": self.options,
            "continent_name": self.continent_name,
            "correct_answer_country": self.country.name,
            "correct_answer_additional_info":
                self.correct_answer_additional_info,
        }


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
