# Generated by Django 3.2.8 on 2021-10-19 08:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kcal_app', '0013_day_base_kcal'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='height',
            field=models.IntegerField(default=0, null=True),
        ),
    ]
