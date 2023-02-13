from django.db import models

from django.db import models
import uuid


class Item(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.PositiveIntegerField()

    def __str__(self):
        return f'{self.name} (id: {self.id})'
