# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
class Rate(models.Model):
  id = models.AutoField(primary_key=True)
  type = models.CharField(max_length=50)
  value = models.FloatField(default=0.0)
  
  def __str__(self):
    return str(self.value)
