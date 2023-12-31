# Generated by Django 4.2.5 on 2023-11-14 11:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("dndapp", "0007_tradelog_gamelog_downtimelog"),
    ]

    operations = [
        migrations.AddField(
            model_name="customuser",
            name="last_online",
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name="userprofile",
            name="public_profile",
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name="userprofile",
            name="show_online_status",
            field=models.BooleanField(default=True),
        ),
    ]
