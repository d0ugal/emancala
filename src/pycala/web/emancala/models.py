from django.db import models

class Player(models.Model):
    name = models.CharField(max_length=20)
    
class ConfiguredPlayer(models.Model):
    player = models.ForeignKey(Player)

class Experement(models.Model):
    players = models.ManyToManyField(Player)
    games = models.IntegerField(default=2)
    rounds = models.IntegerField(default=2)

class Weight(models.Model):
    configured_player = models.ForeignKey(ConfiguredPlayer)
    name = models.CharField(max_length=10)
    value = models.DecimalField(max_digits=10, decimal_places=10,)

class RandomPlayer(Player):
    pass