from django.db import models

from users.models import User
from utils.models import BaseModel


class Car(BaseModel):
    make = models.CharField(max_length=256)
    model = models.CharField(max_length=256)
    year = models.IntegerField()
    description = models.TextField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.make} {self.model} ({self.year})"


class Comment(BaseModel):
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"Comment by {self.author} on {self.car}"
