from tkinter import CASCADE
from django.db import models

from django.db import models

# Create your models here.

class person(models.Model):
    username = models.TextField(unique=True)
    password = models.TextField()
    name = models.TextField()
    email = models.EmailField(unique=True)
    is_authenticated = models.BooleanField(default=False)

    def __str__(self) -> str:
        return "User: "+str(self.id)+" - "+self.name


class todo(models.Model):
    name = models.TextField()
    text = models.TextField()
    date = models.DateField()
    done = models.BooleanField(default=False)
    person_fk = models.ForeignKey(person, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return str(self.id)+" "+self.name
