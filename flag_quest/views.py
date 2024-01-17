import time

from django.http import Http404
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import DetailView, ListView, TemplateView
from django.views.generic.edit import FormView

from flag_quest.additional_function import (question_set_generator,
                                            correct_answer_collector,
                                            get_country_info,
                                            total_result_calculator)
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


class GamePage(FormView):
    context_object_name = "countries"
    template_name = "flag_quest/flag_quest.html"
    question_set = None
    form_class = AnswerForm
    success_url = "/"

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

    def form_invalid(self, form):
        print('Hola')
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        if self.question_set is not None:
            return super().get_context_data(**kwargs)

        self.question_set = question_set_generator("flag",
                                                   "country",
                                                   self.kwargs.get(
                                                       "continent_name"))
        self.form_class = AnswerForm(
            options=self.question_set['options'])

        context = {
            "question": self.question_set,
            "form": self.form_class,
            "continent": self.kwargs.get("continent_name"),
            "correct_answer": correct_answer_collector(self.question_set),
        }
        return context

    def post(self, request, **kwargs):
        answer = Answer()
        answer.save_reply(request.POST)
        time.sleep(2)
        kwargs = {"continent_name": self.kwargs.get("continent_name")}
        redirect_url = reverse("game", kwargs=kwargs)
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
