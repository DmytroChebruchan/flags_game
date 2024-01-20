import time

from django.http import Http404
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView, TemplateView
from django.views.generic.edit import CreateView

from flag_quest.additional_function import (
    get_country_info,
    question_set_generator,
    total_result_calculator,
)
from flag_quest.constants import CONTINENTS
from flag_quest.forms import AnswerForm
from flag_quest.models import Answer, Continent, CountryInfo


class IndexView(TemplateView):
    template_name = "index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["continents"] = CONTINENTS
        return context


class AboutView(TemplateView):
    template_name = "about.html"


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
        if context["continent"]:
            context["continent_description"] = Continent.objects.get(
                name=self.kwargs.get("continent")
            ).description
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


class GamePage(CreateView):
    model = Answer
    form_class = AnswerForm
    success_url = reverse_lazy("game")
    template_name = "flag_quest/flag_quest.html"

    def get_context_data(self, **kwargs):
        continent_name = self.kwargs.get("continent_name")
        question_set = question_set_generator("flag", continent_name)

        form = AnswerForm()
        form.set_params(question_set)

        kwargs["form"] = form
        context = super().get_context_data(
            question_set=question_set, continent=continent_name, **kwargs
        )
        return context

    def form_valid(self, form):
        answer = form.save(commit=False)
        answer.save_reply()
        time.sleep(5)
        return super().form_valid(form)


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
