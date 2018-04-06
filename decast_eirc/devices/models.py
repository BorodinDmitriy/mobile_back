# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
class EIRCDevice(models.Model):
  id = models.IntegerField(primary_key=True)
  type = models.CharField(max_length=50)
  reading = models.CharField(max_length=10)
  date = models.DateTimeField(auto_now=True)
  personal_account = models.CharField(max_length=50)
  serial_number = models.CharField(max_length=50)
  
  def __str__(self):
    return self.reading