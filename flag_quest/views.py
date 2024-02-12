import time

from django.http import Http404
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView, TemplateView
from django.views.generic.edit import CreateView

from flag_quest.additional_functions import (
    QuestionSet,
    add_numbers_to_countries,
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


class GameMenuView(TemplateView):
    template_name = "flag_quest/game_menu.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["continents"] = CONTINENTS
        return context


class CountriesMenuView(TemplateView):
    template_name = "flag_quest/learning_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["continents"] = CONTINENTS
        return context


class AboutView(TemplateView):
    template_name = "flag_quest/about.html"


class ListCounties(ListView):
    model = CountryInfo
    template_name = "flag_quest/list_of_countries.html"
    context_object_name = "countries"
    paginate_by = 20

    def get_queryset(self):
        base_queryset = super().get_queryset()

        continent = self.kwargs.get("continent")
        if continent and continent != "All Continents":
            revised_queryset = base_queryset.order_by("weight").filter(
                continent__iexact=continent
            )
            return revised_queryset

        return base_queryset

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)

        add_numbers_to_countries(self.paginate_by, context_data, "countries")

        context_data["continent"] = self.kwargs.get("continent")

        if context_data["continent"]:
            continent = Continent.objects.get(name=context_data["continent"])
            context_data["continent_description"] = continent.description
        return context_data


class ResultsCountries(ListView):
    model = Answer
    template_name = "flag_quest/results.html"
    context_object_name = "results"
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        add_numbers_to_countries(self.paginate_by, context, "results")
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
    object = None

    def get_context_data(self, **kwargs):
        additional_context = QuestionSet(
            self.kwargs.get("continent_name"), set_flag=True
        ).dict_context()

        kwargs["form"] = AnswerForm().set_params(
            additional_context, add_flag=True
        )

        return super().get_context_data(
            question_set=additional_context, **kwargs
        )

    def form_valid(self, form):
        # saving answer
        answer = form.save(commit=False)
        answer.save_reply()

        # delaying update of page
        time.sleep(4)

        # saving continent
        continent_name = self.kwargs.get("continent_name")
        self.success_url = reverse_lazy(
            "game", kwargs={"continent_name": continent_name}
        )
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
        context["country"] = CountryInfo.objects.get(name=context["object"])
        return context
