# Generated by Django 3.0 on 2020-09-07 08:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('repository', '0003_auto_20200225_1725'),
    ]

    operations = [
        migrations.AlterField(
            model_name='trouble',
            name='ptime',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]