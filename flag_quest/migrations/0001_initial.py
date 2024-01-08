# Generated by Django 4.2.7 on 2023-12-09 20:13

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Answer",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("flag_picture", models.CharField(max_length=500)),
                ("is_correct", models.BooleanField(default=False)),
                ("your_answer", models.CharField(max_length=500)),
                ("correct_answer", models.CharField(max_length=500)),
            ],
        ),
        migrations.CreateModel(
            name="CountryInfo",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=200)),
                ("flag_picture", models.CharField(max_length=500)),
                ("capital", models.CharField(max_length=200, null=True)),
                ("continent", models.CharField(max_length=200, null=True)),
                ("weight", models.IntegerField(default=4)),
            ],
        ),
    ]
