# Generated by Django 3.2.8 on 2021-10-13 11:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('kcal_app', '0002_alter_day_date'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='day',
            unique_together={('date', 'profile')},
        ),
    ]
