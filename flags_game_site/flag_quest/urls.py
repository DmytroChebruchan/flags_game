from django.urls import path
from .views import ListCounties, GamePage, ResultsCountries, IndexView


urlpatterns = [
    path("list_of_coutries", ListCounties.as_view()),
    path("game", GamePage.as_view(), name="game"),
    path("results", ResultsCountries.as_view(), name="results"),
    path("", IndexView.as_view(), name="index"),
]
