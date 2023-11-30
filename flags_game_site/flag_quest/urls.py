from django.urls import include, path
from .views import ListCounties


urlpatterns = [
    path("list_of_coutries", ListCounties.as_view())
]