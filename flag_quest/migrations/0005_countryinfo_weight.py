# Generated by Django 4.2.7 on 2023-12-05 18:25

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("flag_quest", "0004_remove_countryinfo_weight"),
    ]

    operations = [
        migrations.AddField(
            model_name="countryinfo",
            name="weight",
            field=models.IntegerField(default=4),
        ),
    ]