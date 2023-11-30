from django.views.generic import (
    ListView,
)

from flag_quest.models import CountryInfo


# Create your views here.
class ListCounties(ListView):
    model = CountryInfo
    template_name = 'flag_quest/list_of_countries.html'
    context_object_name = 'countries'
