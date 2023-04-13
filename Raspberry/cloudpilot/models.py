from django.db import models
from django.contrib.auth.models import User

class Button(models.Model):
    title = models.CharField(max_length=30)
    isOn = models.BooleanField(default=False)
    command = models.CharField(max_length=300)
    accessLevel = models.IntegerField(default=1)

class Customer(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    userAccessLevel = models.IntegerField(default=0)

    def __str__(self):
        return self.user.username