from django.db import models
from datetime import time
from django.contrib.auth.models import User
from datetime import datetime


class Customer(models.Model):
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    Card = models.ImageField(null=True, blank=True)
    face_picture = models.ImageField(null=True, blank=True)
    name = models.CharField(max_length=200, null=True)
    phone = models.CharField(max_length=200, null=True)
    email = models.CharField(max_length=200, null=True, blank=True)
    LinkFb = models.CharField(max_length=200, null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    approved = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name} approved : {self.approved}"


class offers(models.Model):
    STATUS = (
        ('Sell', 'Sell'),
        ('buy', 'buy')
    )
    Devise = (
        ('paysera', 'paysera'),
        ('wise', 'wise'),
        ('baridimob', 'baridimob')
    )
    customer = models.ForeignKey(Customer, null=True, on_delete=models.SET_NULL)
    title = models.CharField(max_length=20, blank=True)
    date = models.DateField(default=datetime.now)
    created_at = models.DateTimeField(default=datetime.now)
    start_time = models.TimeField(default=time(5))
    duration = models.IntegerField(default=1)
    approve = models.BooleanField(default=False)
    price = models.FloatField(null=True)
    quantity = models.FloatField(default=0)
    lowest = models.FloatField(default=0)
    description = models.CharField(max_length=200, null=True, blank=True)
    devise = models.CharField(max_length=200, null=True, choices=Devise)
    status = models.CharField(max_length=200, null=True, choices=STATUS)
    payment = models.CharField(max_length=200, null=True, choices=Devise)

    def __str__(self):
        return f"{self.title} at {self.created_at}"
