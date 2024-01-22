import random
from random import choice
from typing import List, Optional, Tuple

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


class QuestionSet:
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
        self.country = self.countries[0]
        self.options_setter()
        if set_flag:
            self.flag_setter()

    def countries_setter(self, continent_name: str = None):
        filtered_countries = avail_countries_generator()
        continent_object = continent_getter(continent_name, filtered_countries)
        country_ids = filtered_countries.filter(
            continent_1_id=continent_object
        ).values_list("id", flat=True)
        random_country_ids = random.sample(list(country_ids),
                                           min(5, len(country_ids)))
        self.countries = CountryInfo.objects.filter(id__in=random_country_ids)

    def flag_setter(self):
        self.countries_item = self.country.flag_picture
        self.additional_info_generator("meaning_of_flag")

    def additional_info_generator(self, requirement: str):
        if requirement == "meaning_of_flag":
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
            "correct_answer_additional_info": self.correct_answer_additional_info,
        }


def total_result_calculator():
    answers = Answer.objects.all().count()
    correct_answers = Answer.objects.filter(is_correct=True).count()
    return [correct_answers, answers]


def add_numbers_to_countries(paginate_by, context):
    page_number = context[
        'page_obj'].number if 'page_obj' in context else 1
    # Calculate the counter for each country
    counter_start = (page_number - 1) * paginate_by
    for i, country in enumerate(context['countries'], start=counter_start
                                                            + 1):
        country.counter = i
