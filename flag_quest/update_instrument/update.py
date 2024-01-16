import json

from flag_quest.models import CountryInfo

# Path to your JSON file
file_path = "flag_quest/update_from_file.json"
field_name = "meaning_of_flag"

# Open the JSON file
with open(file_path, "r") as file:
    continents_data = json.load(file)

# Get all countries from the database
countries_from_db = CountryInfo.objects.all()

country_continent_dict = {entry["name"]: entry[field_name] for entry in continents_data}

for country in countries_from_db:
    country_name = country.name
    if country_name in country_continent_dict:
        country.meaning_of_flag = country_continent_dict[country_name]
        country.save()
