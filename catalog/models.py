from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone

import os
import datetime


# def get_image_path(instance, filename):
#   return os.path.join('images', str(instance.id), filename)

class UserProfile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    profile_image = models.ImageField(blank=True, null=True)
    date_reg = models.DateField(auto_now_add=True)
    rating = models.FloatField(editable=False, default=0)

    def publish(self):
        self.date_reg = timezone.now()
        self.save()

    def __str__(self):
        return self.user.username


class Tag(models.Model):
    tag_name = models.TextField()

    def __str__(self):
        return self.tag_name


class Question(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    header = models.CharField(max_length=255)
    body_quest = models.TextField()
    create_date = models.DateTimeField(auto_now_add=True)
    tag = models.ManyToManyField(Tag)
    rating = models.FloatField(default=0, null=True)

    def publish(self):
        self.create_date = timezone.now()
        self.save()

    def __str__(self):
        return self.header


class Answer(models.Model):
    author = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    body_answer = models.TextField()
    create_date = models.DateTimeField(auto_now_add=True)
    rating = models.FloatField(default=0, null=True)
    flag = models.BooleanField(blank=True, default=False)

    def publish(self):
        self.create_date = timezone.now()
        self.save()

    def __str__(self):
        return self.body_answer
