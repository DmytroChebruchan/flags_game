import json
from models import CountryInfo

# Path to your JSON file
file_path = 'countries_and_flags.json'

# Open the JSON file
with open(file_path, 'r') as file:
    data = json.load(file)

# Iterate through each element in the JSON data and add to the database
for entry in data:
    country = entry['country']
    flag = entry['flag']

    # Create and save CountryInfo object
    country_info = CountryInfo.objects.create(name=country, flag_picture=flag)
    country_info.save()
