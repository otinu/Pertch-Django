# Generated by Django 3.2.21 on 2023-09-19 19:52

import datetime
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='PetModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20, validators=[django.core.validators.MinLengthValidator(2)])),
                ('age', models.CharField(max_length=99, validators=[django.core.validators.MinLengthValidator(0)])),
                ('sex', models.BooleanField()),
                ('charmPoint', models.CharField(max_length=1000)),
                ('postCord', models.CharField(max_length=8, validators=[django.core.validators.MinLengthValidator(7)])),
                ('address', models.CharField(max_length=50)),
                ('image', models.ImageField(upload_to='pet_image/')),
                ('created_at', models.DateTimeField(default=datetime.datetime(2023, 9, 20, 4, 52, 36, 362876))),
                ('updated_at', models.DateTimeField(default=datetime.datetime(2023, 9, 20, 4, 52, 36, 362876))),
            ],
        ),
    ]