# Generated by Django 3.2.21 on 2023-10-03 00:57

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('petCommentApp', '0004_auto_20231003_0839'),
    ]

    operations = [
        migrations.AlterField(
            model_name='petcommentmodel',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2023, 10, 3, 9, 57, 23, 55899)),
        ),
        migrations.AlterField(
            model_name='petcommentmodel',
            name='updated_at',
            field=models.DateTimeField(default=datetime.datetime(2023, 10, 3, 9, 57, 23, 55899)),
        ),
    ]