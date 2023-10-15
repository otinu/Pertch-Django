# Generated by Django 3.2.21 on 2023-10-05 02:26

import datetime
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('petApp', '0007_auto_20231005_1120'),
    ]

    operations = [
        migrations.AlterField(
            model_name='petmodel',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2023, 10, 5, 11, 26, 38, 771324)),
        ),
        migrations.AlterField(
            model_name='petmodel',
            name='post_cord',
            field=models.IntegerField(validators=[django.core.validators.MaxValueValidator(9999999)]),
        ),
        migrations.AlterField(
            model_name='petmodel',
            name='updated_at',
            field=models.DateTimeField(default=datetime.datetime(2023, 10, 5, 11, 26, 38, 771324)),
        ),
    ]