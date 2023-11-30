from django.db import models


# Create your models here.
class CountryInfo(models.Model):
    name = models.CharField(max_length=200)
    flag_picture = models.CharField(max_length=500)

    def __str(self):
        return self.name
