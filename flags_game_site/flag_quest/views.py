from django.views.generic import ListView, TemplateView
from django.views.generic.edit import FormView
from django.shortcuts import render, redirect

from flag_quest.forms import FlagForm
from flag_quest.models import CountryInfo, Answer
from flag_quest.additional_function import (
    context_generator,
    adding_correct_answers,
)


class IndexView(TemplateView):
    template_name = 'index.html'


# Create your views here.
class ListCounties(ListView):
    model = CountryInfo
    template_name = "flag_quest/list_of_countries.html"
    context_object_name = "countries"


class ResultsCountries(ListView):
    model = Answer
    template_name = "flag_quest/results.html"
    context_object_name = "results"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        adding_correct_answers(context)
        return context

    def post(self, request):
        if "clean" in request.POST:
            Answer.objects.all().delete()
            return redirect('results')


def options_generator(question):
    return [
        (option[0], option[0]) for option in question["options"]
    ]


def correct_answer_generator(question):
    options = question['options']
    correct_answer = ''
    for option in options:
        if option[1] == 'correct':
            correct_answer = option[0]
            break

    return correct_answer


class GamePage(FormView):
    model = CountryInfo
    context_object_name = "countries"
    template_name = "flag_quest/flag_quest.html"
    question = context_generator("flag", "country")
    form_class = FlagForm(options=options_generator(question))
    correct_answer = correct_answer_generator(question)

    def get_context_data(self, **kwargs):
        context = {"question": self.question, "form": self.form_class}
        return context

    def post(self, request):
        if "check" in request.POST:
            return redirect("game")

        elif "next" in request.POST:
            return render(
                request,
                self.template_name,
                {"question": self.question, "form": self.form},
            )
