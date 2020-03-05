# Generated by Django 3.0.3 on 2020-03-01 09:18

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tag_name', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('email', models.EmailField(max_length=254)),
                ('nickname', models.CharField(max_length=25, unique=True)),
                ('password', models.CharField(max_length=25)),
                ('date_reg', models.DateField(default=datetime.date.today)),
                ('rating', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('header', models.TextField()),
                ('body_quest', models.TextField()),
                ('create_date', models.DateTimeField(default=datetime.date.today)),
                ('rating', models.FloatField()),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='catalog.UserProfile')),
                ('tag', models.ManyToManyField(to='catalog.Tag')),
            ],
        ),
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('body_answer', models.TextField()),
                ('create_date', models.DateTimeField(default=datetime.date.today)),
                ('rating', models.FloatField()),
                ('flag', models.BooleanField()),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='catalog.UserProfile')),
                ('question', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='catalog.Question')),
                ('tag', models.ManyToManyField(to='catalog.Tag')),
            ],
        ),
    ]
