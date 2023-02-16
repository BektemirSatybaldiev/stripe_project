from django.contrib.auth.models import User
from django.db import models


class Item(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.PositiveIntegerField()
    currency = models.CharField(max_length=3, choices=(("USD", "USD"), ("EUR", "EUR")), default='USD')

    def __str__(self):
        return f'{self.name} (id: {self.id})'


class Discount(models.Model):
    name = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f'{self.name}'


class Tax(models.Model):
    name = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f'{self.name}'


class Order(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    items = models.ManyToManyField(Item)
    discount = models.ForeignKey(Discount, on_delete=models.SET_NULL, null=True, blank=True)
    tax = models.ForeignKey(Tax, on_delete=models.SET_NULL, null=True, blank=True)

    def total_amount(self):
        items_total = sum([item.price for item in self.items.all()])
        discount = self.discount.amount if self.discount else 0
        tax = self.tax.amount if self.tax else 0
        total = items_total - discount + tax
        return total

    def __str__(self):
        return f"Items: {self.items.nam}, price: {self.total_amount()}$, user_id: {self.user.id}"



