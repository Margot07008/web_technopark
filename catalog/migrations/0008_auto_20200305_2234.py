# Generated by Django 3.0.3 on 2020-03-05 19:34

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0007_auto_20200305_2232'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='create_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2020, 3, 5, 19, 34, 28, 471552, tzinfo=utc), null=True),
        ),
    ]