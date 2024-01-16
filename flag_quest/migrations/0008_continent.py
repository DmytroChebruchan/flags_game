# Generated by Django 4.2.7 on 2024-01-16 16:36

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("flag_quest", "0007_countryinfo_weight"),
    ]

    operations = [
        migrations.CreateModel(
            name="Continent",
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
                ("description", models.CharField(max_length=1000, null=True)),
            ],
        ),
    ]