# Generated by Django 3.2.8 on 2021-10-20 12:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('kcal_app', '0015_day_day_weight'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='plan',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='kcal_app.plan'),
        ),
        migrations.DeleteModel(
            name='Recipe',
        ),
    ]
