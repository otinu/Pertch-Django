# Generated by Django 3.2.21 on 2023-10-04 06:26

import datetime
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('petApp', '0004_auto_20230924_0556'),
    ]

    operations = [
        migrations.AlterField(
            model_name='petmodel',
            name='age',
            field=models.IntegerField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(99)]),
        ),
        migrations.AlterField(
            model_name='petmodel',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2023, 10, 4, 15, 26, 32, 123325)),
        ),
        migrations.AlterField(
            model_name='petmodel',
            name='updated_at',
            field=models.DateTimeField(default=datetime.datetime(2023, 10, 4, 15, 26, 32, 123325)),
        ),
    ]
