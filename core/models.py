from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class User(AbstractUser):

    profile_image = models.ImageField(blank=True, null=True)
    # date_reg = models.DateField(auto_now_add=True)
    rating = models.FloatField(editable=False, default=0)

    # def publish(self):
    #     self.create_date = timezone.now()
    #     self.save()

    def __str__(self):
        return self.username
