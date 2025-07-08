from django.db import models

# Create your models here.
class Customer(models.Model):
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=20)
    email = models.EmailField()
    mobile = models.CharField(max_length=12, default=90)
    address = models.CharField(max_length=100)
    role = models.CharField(max_length=10, default='CUSTOMER')

    def __str__(self):
        return f"{self.username}, {self.password}"