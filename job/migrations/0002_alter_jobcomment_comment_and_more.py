# Generated by Django 5.0.4 on 2024-06-28 15:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("job", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="jobcomment",
            name="comment",
            field=models.CharField(max_length=1000),
        ),
        migrations.AlterField(
            model_name="jobstatusupdate",
            name="update_text",
            field=models.CharField(default="Initialize Job", max_length=200),
        ),
    ]
