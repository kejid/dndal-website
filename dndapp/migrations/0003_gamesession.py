# Generated by Django 4.2.5 on 2023-11-13 21:12

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("dndapp", "0002_character"),
    ]

    operations = [
        migrations.CreateModel(
            name="GameSession",
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
                ("date_of_game", models.DateTimeField()),
                ("description", models.TextField()),
                ("location", models.CharField(max_length=100)),
                ("game_tier", models.IntegerField()),
                (
                    "master",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="mastered_sessions",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "players",
                    models.ManyToManyField(
                        related_name="participated_sessions",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]
