# Generated by Django 5.0.4 on 2024-05-07 09:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('job', '0003_company_alter_job_company'),
    ]

    operations = [
        migrations.AlterField(
            model_name='company',
            name='founded',
            field=models.IntegerField(),
        ),
    ]