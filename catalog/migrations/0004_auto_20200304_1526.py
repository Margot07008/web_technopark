# Generated by Django 3.0.3 on 2020-03-04 12:26

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0003_auto_20200304_1446'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='profile_image',
            field=models.ImageField(blank=True, null=True, upload_to='../catalog/static/images'),
        ),
        migrations.AlterField(
            model_name='question',
            name='create_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2020, 3, 4, 12, 26, 35, 352844, tzinfo=utc), null=True),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='rating',
            field=models.FloatField(default=0, editable=False),
        ),
    ]
