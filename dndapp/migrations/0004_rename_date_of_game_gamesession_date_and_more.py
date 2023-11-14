# Generated by Django 4.2.5 on 2023-11-14 09:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("dndapp", "0003_gamesession"),
    ]

    operations = [
        migrations.RenameField(
            model_name="gamesession", old_name="date_of_game", new_name="date",
        ),
        migrations.RenameField(
            model_name="gamesession", old_name="game_tier", new_name="tier",
        ),
        migrations.AlterField(
            model_name="gamesession",
            name="location",
            field=models.CharField(max_length=200),
        ),
    ]