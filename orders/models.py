from django.db import models
from django.contrib.auth.models import User


class Pizza(models.Model):
    name = models.CharField(max_length=64)
    description = models.CharField(max_length=100)
    small_price = models.FloatField(max_length=5, default=0)
    medium_price = models.FloatField(max_length=5, default=0)
    large_price = models.FloatField(max_length=5, default=0)

    def __str__(self):
        return f"{self.name}"


class Topping(models.Model):
    name = models.CharField(max_length=20)
    description = models.CharField(max_length=100)
    price = models.FloatField(max_length=4)

    def __str__(self):
        return f"{self.name} - ₹{self.price}"


class Status(models.Model):
    title = models.CharField(max_length=10)

    def __str__(self):
        return f"{self.title}"


class Order(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    pizza = models.ForeignKey(Pizza, on_delete=models.CASCADE)
    size = models.CharField(max_length=10, default="medium")
    toppings = models.ManyToManyField(Topping, blank=True)
    price = models.FloatField(max_length=6)
    status = models.ForeignKey(Status, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user_id} - ₹{self.price} ({self.status})"

