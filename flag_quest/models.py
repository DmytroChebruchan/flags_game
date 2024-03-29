from django.db import models


class Continent(models.Model):
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=1000, null=True)


class CountryInfo(models.Model):
    name = models.CharField(max_length=200)
    flag_picture = models.CharField(max_length=500)
    capital = models.CharField(max_length=200, null=True)
    continent = models.CharField(max_length=200, null=True)
    meaning_of_flag = models.CharField(max_length=1200)
    continent_1 = models.ForeignKey(
        Continent, on_delete=models.DO_NOTHING, null=True
    )

    weight = models.IntegerField(default=4, null=True)

    def __str__(self):
        return self.name


class Answer(models.Model):
    flag_picture = models.CharField(max_length=500)
    is_correct = models.BooleanField(default=False)
    your_answer = models.CharField(max_length=500)
    correct_answer = models.CharField(max_length=500)

    def __str__(self):
        return f"{self.your_answer}"

    def save_reply(self):
        self.answer_checker()
        self.save()

    def answer_checker(self):
        country = CountryInfo.objects.get(flag_picture=self.flag_picture)
        self.correct_answer = country.name
        self.is_correct = self.correct_answer == self.your_answer
