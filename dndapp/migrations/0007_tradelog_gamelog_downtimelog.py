# Generated by Django 4.2.5 on 2023-11-14 10:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("dndapp", "0006_notification"),
    ]

    operations = [
        migrations.CreateModel(
            name="TradeLog",
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
                ("traded_with", models.CharField(max_length=100)),
                ("items_received", models.TextField()),
                ("items_given", models.TextField()),
                ("downtime_spent", models.IntegerField()),
                ("trade_date", models.DateTimeField(auto_now_add=True)),
                (
                    "character",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="dndapp.character",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="GameLog",
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
                ("date_played", models.DateTimeField()),
                ("adventure_code", models.CharField(max_length=100)),
                ("adventure_name", models.CharField(max_length=200)),
                ("downtime_earned", models.IntegerField()),
                ("gold_earned", models.DecimalField(decimal_places=2, max_digits=10)),
                ("items_dropped", models.TextField()),
                ("level_gained", models.BooleanField(default=False)),
                ("faction_rank_increase", models.BooleanField(default=False)),
                ("story_awards", models.TextField()),
                (
                    "character",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="dndapp.character",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="DowntimeLog",
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
                ("activity_description", models.TextField()),
                ("downtime_spent", models.IntegerField()),
                ("log_date", models.DateTimeField(auto_now_add=True)),
                (
                    "character",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="dndapp.character",
                    ),
                ),
            ],
        ),
    ]
