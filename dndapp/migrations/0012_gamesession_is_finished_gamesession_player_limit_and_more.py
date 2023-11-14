# Generated by Django 4.2.5 on 2023-11-14 13:13

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("dndapp", "0011_rename_description_complaint_details_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="gamesession",
            name="is_finished",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="gamesession",
            name="player_limit",
            field=models.IntegerField(default=6),
        ),
        migrations.CreateModel(
            name="GameApplication",
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
                ("status", models.CharField(default="Pending", max_length=100)),
                (
                    "character",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="dndapp.character",
                    ),
                ),
                (
                    "game_session",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="applications",
                        to="dndapp.gamesession",
                    ),
                ),
                (
                    "player",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]