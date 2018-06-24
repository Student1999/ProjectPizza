from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey,GenericRelation

User = get_user_model()
# Create your models here.

class RegularPizza(models.Model):
    name = models.CharField(max_length=32)
    small = models.CharField(max_length=8)
    large = models.CharField(max_length=8)
    def __str__(self):
        return f" {self.name}, small:{self.small}, large: {self.large}"

class SicilianPizza(models.Model):
    name = models.CharField(max_length=32)
    small = models.CharField(max_length=8)
    large = models.CharField(max_length=8)
    def __str__(self):
        return f" {self.name}, small:{self.small}, large: {self.large}"

class Toppings(models.Model):
    name = models.CharField(max_length=32)
    def __str__(self):
        return f" {self.name}"

class DinnerPlatters(models.Model):
    name = models.CharField(max_length=32)
    small = models.CharField(max_length=8)
    large = models.CharField(max_length=8)
    def __str__(self):
        return f" {self.name}, small:{self.small}, large: {self.large}"

class Subs(models.Model):
    name = models.CharField(max_length=32)
    small = models.CharField(max_length=8, null=True)
    large = models.CharField(max_length=8)
    def __str__(self):
        return f" {self.name}, small:{self.small}, large: {self.large}"

class ExtraForSubs(models.Model):
    name = models.CharField(max_length=32)
    small = models.CharField(max_length=8)
    large = models.CharField(max_length=8)
    def __str__(self):
        return f" {self.name}, small:{self.small}, large: {self.large}"

class Salad(models.Model):
    name = models.CharField(max_length=32)
    small = models.CharField(max_length=8)
    def __str__(self):
        return f" {self.name}, small {self.small}"

class Pasta(models.Model):
    name = models.CharField(max_length=32)
    small = models.CharField(max_length=8)
    def __str__(self):
        return f" {self.name}, small {self.small}"

class Meals(models.Model):
    price = models.CharField(max_length=8)

    #if Scilian and RegularPizza have been picked to add cart then toppings should provide
    toppings = models.ManyToManyField(Toppings,blank=True,related_name="meals")

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()

    order = GenericForeignKey('content_type','object_id')

    def __str__(self):
        return f"{self.order} {self.price}"

class Cart(models.Model):
    customer = models.ForeignKey(User,blank=True,on_delete=models.CASCADE, related_name="cart_user")
    order = models.ManyToManyField(Meals,blank=True, related_name="cart_customer_order")
    #order = GenericRelation(Meals)
    def __str__(self):
        return f"{self.customer} {self.order.all()}"

class Orders(models.Model):
    customer = models.ForeignKey(User,blank=True,on_delete=models.CASCADE, related_name="user")
    order = models.ManyToManyField(Meals,blank=True, related_name="customer_order")

    def __str__(self):
        return f"{self.customer} {self.order.all()}"
