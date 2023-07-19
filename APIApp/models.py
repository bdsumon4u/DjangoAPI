from django.db import models


# Create your models here.

class Product(models.Model):
    owner = models.ForeignKey('auth.User', related_name='snippets', on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=255)
    price = models.FloatField()
    description = models.TextField()