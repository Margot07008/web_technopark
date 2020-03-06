from django.db import models
from django.utils import timezone


import os
import datetime

#def get_image_path(instance, filename):
#   return os.path.join('images', str(instance.id), filename)

# Create your models here.
class UserProfile(models.Model):


    id = models.AutoField(primary_key=True)
    email = models.EmailField()
    nickname = models.CharField(max_length = 25, unique=True)
    password = models.CharField(max_length = 25)
   # profile_image = models.ImageField(upload_to='../catalog/static/images', blank=True, null=True)
    date_reg = models.DateField(blank=True, null=True)
    rating = models.FloatField(editable=False, default=0)

    def publish(self):
        self.date_reg = timezone.now()
        self.save()

    def __str__(self):
        return self.nickname


class Tag(models.Model):
    tag_name = models.TextField()

    def __str__(self):
        return self.tag_name


class Question(models.Model):

    author = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    header = models.TextField()
    body_quest = models.TextField()
    create_date = models.DateTimeField(default=timezone.now(), blank=True, null=True)
    tag = models.ManyToManyField(Tag)
    rating = models.FloatField(null=True)

    def publish(self):
        self.create_date = timezone.now()
        self.save()

    def __str__(self):
        return self.header


class Answer(models.Model):

    author = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    question = models.OneToOneField(Question, on_delete=models.CASCADE)
    body_answer = models.TextField()
    create_date = models.DateTimeField(blank=True, null=True)
    rating = models.FloatField()
    tag = models.ManyToManyField(Tag)
    flag = models.BooleanField()

    def publish(self):
        self.create_date = timezone.now()
        self.save()

    def __str__(self):
        return self.body_answer

