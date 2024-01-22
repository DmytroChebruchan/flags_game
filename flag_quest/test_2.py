# from django.test import TestCase, Client
# from django.urls import reverse
# from unittest.mock import patch, MagicMock
# from flag_quest.views import ListCounties
# from flag_quest.models import CountryInfo, Continent, Answer
#
#
# class TestViews(TestCase):
#     def setUp(self):
#         self.client = Client()
#         # self.employees = EmployeeFactory.create_batch(10)
#
#     @patch("flag_quest.models.Answer")
#     @patch("flag_quest.models.Continent")
#     @patch("flag_quest.models.CountryInfo")
#     def test_list_countries_view(self, mock_country_info, mock_continent,
#                                  mock_answer):
#         # Mock the behavior of your models
#         mock_country_info.objects.get.return_value = MagicMock()
#         mock_continent.objects.get.return_value = MagicMock()
#         mock_answer.objects.get.return_value = MagicMock()
#
#         # Mock the data for your models
#         mock_country_info_data = {"name": "TestCountry",
#                                   "flag_picture": "test.jpg",
#                                   "continent": "Europe"}
#         mock_country_info.objects.filter.return_value = [
#             MagicMock(**mock_country_info_data)]
#
#         # Mock the Continent model behavior for existing and non-existing cases
#         mock_continent_data = {"name": "Europe",
#                                "description": "Test description"}
#         mock_continent_object = MagicMock(**mock_continent_data)
#         mock_continent.objects.get.return_value = mock_continent_object
#
#         # Update the URL to include the continent parameter
#         url = reverse("countries_by_continent", args=["Europe"])
#         response_europe = self.client.get(url)
#
#         self.assertEqual(response_europe.status_code, 200)
#         self.assertTemplateUsed(response_europe,
#                                 "flag_quest/list_of_countries.html")
#
#         # Assert that your models' methods were called as expected
#         mock_country_info.objects.get.assert_called_once_with(
#             flag_picture="test.jpg")
#         mock_continent.objects.get.assert_called_once_with(name="Europe")
