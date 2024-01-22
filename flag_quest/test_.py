from django.test import Client, TestCase
from django.urls import reverse


# from flag_quest.models import Answer, CountryInfo


class TestViews(TestCase):
    def setUp(self):
        self.client = Client()

    def test_index_view(self):
        response = self.client.get(reverse("index"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "index.html")

    def test_results_view(self):
        response = self.client.get(reverse("results"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "flag_quest/results.html")

    # def test_list_countries_view(self):
    #     # Update the URL to include the continent parameter
    #     url = reverse("countries_by_continent", args=["Europe"])
    #     response = self.client.get(url)
    #
    #     self.assertEqual(response.status_code, 200)
    #     self.assertTemplateUsed(response, "flag_quest/list_of_countries.html")
    #
    # def test_results_countries_view(self):
    #     response = self.client.get(reverse("results"))
    #     self.assertEqual(response.status_code, 200)
    #     self.assertTemplateUsed(response, "flag_quest/results.html")
    #
    # def test_game_page_view_get(self):
    #     response = self.client.get(
    #         reverse("game", kwargs={"continent_name": "Europe"}))
    #     self.assertEqual(response.status_code, 200)
    #     # self.assertTemplateUsed(response, 'flag_quest/flag_quest.html')
