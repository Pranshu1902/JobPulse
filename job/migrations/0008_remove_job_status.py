# Generated by Django 5.0.4 on 2024-06-03 11:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("job", "0007_alter_company_id_alter_job_id_alter_jobcomment_id_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="job",
            name="status",
        ),
    ]
