from django.test import Client, TestCase
from django.urls import reverse


class TestViews(TestCase):
    def setUp(self):
        self.client = Client()

    def test_index_view(self):
        response = self.client.get(reverse("index"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.template_name[0], "index.html")

    def test_results_view(self):
        response = self.client.get(reverse("results"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.template_name[0], "flag_quest/results.html")

    def test_about_view(self):
        response = self.client.get(reverse("about"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.template_name[0], "flag_quest/about.html")
