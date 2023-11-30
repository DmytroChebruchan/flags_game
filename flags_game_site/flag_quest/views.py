from django.views.generic import ListView, TemplateView
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


class GamePage(ListView):
    model = CountryInfo
    context_object_name = "countries"
    template_name = "flag_quest/flag_quest.html"
    form = None
    question = None
    correct_answer = None

    def get(self, request, **kwargs):

        self.question = context_generator("flag", "country")
        self.form = FlagForm(options=self.options_generator())
        self.correct_answer = self.correct_answer_generator()

        return render(
            request,
            self.template_name,
            {"question": self.question, "form": self.form},
        )

    def correct_answer_generator(self):
        options = self.question['options']
        correct_answer = ''
        for option in options:
            if option[1] == 'correct':
                correct_answer = option[0]
                break

        return correct_answer

    def options_generator(self):
        return [
            (option[0], option[0]) for option in self.question["options"]
        ]

    def post(self, request):
        if "check" in request.POST:
            return redirect("game")

        elif "next" in request.POST:
            return render(
                request,
                self.template_name,
                {"question": self.question, "form": self.form},
            )
