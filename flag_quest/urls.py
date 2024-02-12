from django.urls import path

from .views import (AboutView, CountriesMenuView, CountryDetailsView,
                    GameMenuView, GamePage, IndexView, ListCounties,
                    ResultsCountries)

urlpatterns = [
    path("list_of_countries/", ListCounties.as_view(), name="all_countries"),
    path(
        "list_of_countries/<str:continent>",
        ListCounties.as_view(),
        name="countries_by_continent",
    ),
    path(
        "country_details/<str:country>",
        CountryDetailsView.as_view(),
        name="country_details",
    ),
    path("game/", GamePage.as_view(), name="game"),
    path("game/<path:continent_name>", GamePage.as_view(), name="game"),
    path("results", ResultsCountries.as_view(), name="results"),
    path("", IndexView.as_view(), name="index"),
    path("about", AboutView.as_view(), name="about"),
    path("countries_menu", CountriesMenuView.as_view(), name="countries_menu"),
    path("games_menu", GameMenuView.as_view(), name="games_menu"),
]
