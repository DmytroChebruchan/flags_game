import time

from django.shortcuts import redirect
from django.http import Http404
from django.urls import reverse
from django.views.generic import DetailView, ListView, TemplateView
from django.views.generic.edit import FormView

from flag_quest.additional_function import (
    context_generator,
    correct_answer_collector,
    get_country_info,
    options_generator,
    save_reply_of_user,
    total_result_calculator,
)
from flag_quest.constants import CONTINENTS
from flag_quest.forms import AnswerForm
from flag_quest.models import Answer, CountryInfo


class IndexView(TemplateView):
    template_name = "index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["continents"] = CONTINENTS
        return context


class AboutView(TemplateView):
    template_name = "about.html"


# Create your views here.
class ListCounties(ListView):
    model = CountryInfo
    template_name = "flag_quest/list_of_countries.html"
    context_object_name = "countries"

    def get_queryset(self):
        queryset = super().get_queryset().order_by("weight")
        continent = self.kwargs.get("continent")

        if continent and continent != "All Continents":
            queryset = queryset.filter(continent__iexact=continent)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["show_continent"] = False if self.kwargs.get(
            "continent") else True
        context["continent"] = self.kwargs.get("continent")
        return context


class ResultsCountries(ListView):
    model = Answer
    template_name = "flag_quest/results.html"
    context_object_name = "results"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["total_result"] = total_result_calculator()
        return context

    def post(self, request):
        if "clean" in request.POST:
            Answer.objects.all().delete()
            return redirect("results")


class GamePage(FormView):
    model = CountryInfo
    context_object_name = "countries"
    template_name = "flag_quest/flag_quest.html"
    continent = "Europe"
    question = None
    form_class = None
    correct_answer = None
    success_url = "/"

    def get_context_data(self, **kwargs):
        self.continent = self.kwargs.get("continent_name")
        self.question = context_generator("flag", "country", self.continent)
        self.form_class = AnswerForm(options=options_generator(self.question))

        context = {
            "question": self.question,
            "form": self.form_class,
            "continent": self.continent,
            "correct_answer": correct_answer_collector(self.question),
        }
        return context

    def post(self, request, **kwargs):
        self.continent = self.kwargs.get("continent_name")
        returned_request = request.POST
        save_reply_of_user(returned_request)

        time.sleep(2.0)

        redirect_url = reverse("game",
                               kwargs={"continent_name": self.continent})
        return redirect(redirect_url)


class CountryDetailsView(DetailView):
    template_name = "flag_quest/country_details.html"
    model = CountryInfo

    def get_object(self, queryset=None):
        country_name = self.kwargs.get("country")
        try:
            return self.model.objects.get(name=country_name)
        except self.model.DoesNotExist:
            raise Http404("Country not found")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["country"] = get_country_info(context["object"])
        return context
