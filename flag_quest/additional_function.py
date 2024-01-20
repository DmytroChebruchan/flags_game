import random
from random import choice
from typing import Optional, Union, List, Tuple

from django.core.exceptions import ObjectDoesNotExist
from django.db.models import QuerySet

from flag_quest.models import Answer, Continent, CountryInfo


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

    def __init__(self, continent_name: Optional[str] = None,
                 set_flag: bool = False):
        self.continent_name = continent_name
        self.countries_setter(continent_name)
        self.country = self.countries.first()
        self.options_setter()
        if set_flag:
            self.flag_setter()
        print(f'After flag is setted Country is: {list(self.countries)}')
        print(f'After flag is setted Country: {self.country.name}')

    def countries_setter(self, continent_name: str = None):
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


def get_country_attribute(country, attr):
    attribute_mapping = {
        "flag": "flag_picture",
        "capital": "capital",
        "name": "name",
        "meaning_of_flag": "meaning_of_flag",
    }
    attribute = attribute_mapping.get(attr)
    return getattr(country, attribute, None) if attribute else None


def total_result_calculator():
    answers = Answer.objects.all().count()
    correct_answers = Answer.objects.filter(is_correct=True).count()
    return [correct_answers, answers]


def get_country_info(country_name):
    try:
        return CountryInfo.objects.get(name=country_name)
    except CountryInfo.DoesNotExist:
        return "Country not found"
