from django.db import models
from django.utils import timezone
from user.models import CustomUser
# Create your models here.


class Event(models.Model):
    name = models.CharField(max_length = 30)
    created_by = models.ForeignKey(CustomUser, on_delete = models.CASCADE)
    created_at = models.DateTimeField(default = timezone.now)

class EventUser(models.Model):
    event = models.ForeignKey(Event, on_delete = models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete = models.CASCADE)

class Pass(models.Model):
    event = models.ForeignKey(Event, on_delete = models.CASCADE)
    name = models.CharField(max_length = 30)
    cost = models.IntegerField()

class Customer(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    email = models.EmailField()
    name = models.CharField(max_length = 50)
    code = models.CharField(max_length = 150)

class Transaction(models.Model):
    customer = models.ForeignKey(Customer, on_delete = models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    PASS = models.ForeignKey(Pass, on_delete=models.CASCADE)
    count = models.IntegerField()
    created_by = models.ForeignKey(CustomUser, on_delete = models.CASCADE)
    datetime = models.DateTimeField(default = timezone.now)
