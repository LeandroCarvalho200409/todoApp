from cgitb import text
from datetime import date
from django.db import models

# Create your models here.

class user(models.Model):
    username = models.TextField(unique=True)
    password = models.TextField()
    name = models.TextField()
    email = models.TextField()


class todo(models.Model):
    name = models.TextField()
    text = models.TextField()
    date = models.DateField()
    user_fk = models.ForeignKey(user, on_delete=models.CASCADE)
