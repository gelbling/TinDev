# Generated by Django 4.1.3 on 2022-12-06 18:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("tindev", "0005_createpost_recruiter"),
    ]

    operations = [
        migrations.AddField(
            model_name="candidateprofile",
            name="interested",
            field=models.ManyToManyField(to="tindev.createpost"),
        ),
    ]