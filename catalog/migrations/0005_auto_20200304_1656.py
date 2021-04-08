# Generated by Django 3.0.3 on 2020-03-04 13:56

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0004_auto_20200304_1526'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='profile_image',
        ),
        migrations.AlterField(
            model_name='question',
            name='create_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2020, 3, 4, 13, 56, 18, 360811, tzinfo=utc), null=True),
        ),
    ]