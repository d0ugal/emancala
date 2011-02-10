# HACK: Django doesn't directly support the use of the ORM outside of
# a Django project. If this module is imported outside of the django
# project the django enviroment needs to be set up.

import os
import sys
from os.path import dirname

if 'DJANGO_SETTINGS_MODULE' not in os.environ:
    # put settings.py on path
    sys.path.insert(0, (dirname(__file__) or '.') + '/../..') 
    os.environ['DJANGO_SETTINGS_MODULE'] = 'pycala.web.settings'
    
# HACK END

import datetime

from django.db import models

class Neuron(models.Model):
    
    binary = models.CharField(max_length=112,unique=True)
    probability = models.FloatField(default=0.0,)
    won = models.IntegerField(default=0,)
    lost = models.IntegerField(default=0,)
    draw = models.IntegerField(default=0,)
    end_visited = models.BooleanField(default=False)
    found = models.DateTimeField(default=datetime.datetime.now())
    updated = models.DateTimeField()
    visited = models.IntegerField(default=0)
    
    class Meta:
        ordering = ('-probability',)
    
    def save(self, *args, **kwargs):
        self.visited += 1
        self.updated = datetime.datetime.now()
        super(Neuron, self).save(*args, **kwargs)
    
    def percent_won(self):
        total = self.won + self.lost + self.draw
        return (self.won/total)*100

class Log(models.Model):
    date = models.DateTimeField(default=datetime.datetime.now())
    result = models.IntegerField(choices=((-1,'lost'),(0,'drawn'),(1,'won'),))