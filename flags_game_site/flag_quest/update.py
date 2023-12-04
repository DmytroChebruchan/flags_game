import json

from flag_quest.models import CountryInfo

# Path to your JSON file
file_path = "/Users/dmitriychebruchan/programming/flags_game/flags_game_site/flag_quest/country_continents.json"


# Open the JSON file
with open(file_path, "r") as file:
    continents_data = json.load(file)

# Get all countries from the database
countries_from_db = CountryInfo.objects.all()

# Create a dictionary with country names as keys and continents as values
country_continent_dict = {
    entry["country"]: entry["continent"] for entry in continents_data
}

for country in countries_from_db:
    country_name = country.name
    if country_name in country_continent_dict:
        country.continent = country_continent_dict[country_name]
        country.save()
