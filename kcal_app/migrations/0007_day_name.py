# Generated by Django 3.2.8 on 2021-10-18 08:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kcal_app', '0006_alter_day_unique_together'),
    ]

    operations = [
        migrations.AddField(
            model_name='day',
            name='name',
            field=models.CharField(default='', max_length=2),
        ),
    ]
