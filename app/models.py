from django.db import models
from django.contrib.auth.models import User


class Game(models.Model):
    title = models.CharField(max_length=100)
    genre = models.CharField(max_length=100)
    image_url = models.CharField(max_length=250, default="image")
    price = models.FloatField(max_length=10)
    about = models.TextField()

    def __str__(self):
        return self.title


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    games = models.ForeignKey(Game, on_delete=models.CASCADE)

    def __str__(self):
        return self.games.title
