# Generated by Django 3.0.3 on 2020-03-05 13:18

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0005_auto_20200304_1656'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='create_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2020, 3, 5, 13, 18, 37, 622432, tzinfo=utc), null=True),
        ),
    ]
