from django.shortcuts import redirect
from django.views.generic import ListView, TemplateView
from django.views.generic.edit import FormView
from django.urls import reverse

from flag_quest.additional_function import (context_generator,
                                            options_generator,
                                            save_reply_of_user,
                                            total_result_calculator)
from flag_quest.forms import AnswerForm
from flag_quest.models import Answer, CountryInfo


class IndexView(TemplateView):
    template_name = "index.html"


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
    question = None
    form_class = None
    correct_answer = None
    continent = ''
    success_url = "/"

    def get_context_data(self, *args, **kwargs):
        self.continent = self.kwargs.get('continent_name')
        self.question = context_generator("flag", "country", self.continent)
        self.form_class = AnswerForm(options=options_generator(self.question),
                                     flag=self.question)

        context = {"question": self.question,
                   "form": self.form_class,
                   "continent": self.continent}
        return context

    def post(self, request, **kwargs):
        returned_request = request.POST
        save_reply_of_user(returned_request)
        continent = kwargs['continent_name']
        redirect_url = reverse('game',
                               kwargs={'continent_name': continent})
        return redirect(redirect_url)
