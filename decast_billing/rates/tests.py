# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework.reverse import reverse
from django.test import TestCase,Client
from rest_framework import status
from rest_framework.test import APITestCase,APIClient



from rates.models import Rate

# Create your tests here.
class RateListTestCase(APITestCase):
  def setUp(self):
    self.url = "/rates/"
    self.rate={
      'type' : 'test',
      'value' : 999.0
      }
  def test_rate_post_good(self):
    response = self.client.post(
            self.url,
            self.rate
        )
    self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    self.assertEqual(len(Rate.objects.all()), 1)
    rate = Rate.objects.get(type=self.rate["type"])
    self.assertEqual(str(self.rate['value']), rate.__str__())
  def test_rate_post_bad(self):
    del self.rate["type"]
    response = self.client.post(
            self.url,
            self.rate
        )
    self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    self.assertEqual(len(Rate.objects.all()), 0)
  def test_rate_get_good(self):
    response = self.client.post(
            self.url,
            self.rate
        )
    self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    self.assertEqual(len(Rate.objects.all()), 1)
    response = self.client.get(self.url)
    self.assertEqual(len(response.data), 1)

class RateDetailTestCase(APITestCase):
  def setUp(self):
    self.rates_url = "/rates/"
    self.rate={
      'type' : 'test',
      'value' : 999.0
      }
    self.new_rate={
      'type' : 'test',
      'value' : 888.0
      }
    response = self.client.post(
            self.rates_url,
            self.rate
        )
    self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    self.url="/rates/1/"
  def test_rate_get_good(self):
    response = self.client.get(self.url)
    self.assertEqual(len(response.data), 3)
    self.assertEqual(response.data["id"], 1)
    self.assertEqual(response.data["type"], "test")
  def test_rate_put_good(self):
    response = self.client.put(self.url,self.new_rate)
    self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    response = self.client.get(self.url)
    self.assertEqual(len(response.data), 3)
    self.assertEqual(response.data["id"], 1)
    self.assertEqual(response.data["value"], 888.0)
  def test_rate_put_bad(self):
    del self.new_rate["value"]
    response = self.client.put(self.url,self.new_rate)
    self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    response = self.client.get(self.url)
    self.assertEqual(len(response.data), 3)
    self.assertEqual(response.data["id"], 1)
    self.assertEqual(response.data["value"], 999.0)
  def test_rate_delete_good(self):
    response = self.client.delete(self.url)
    self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
    response = self.client.get(self.url)
    self.assertEqual(len(response.data), 1)
    self.assertEqual(response.data["detail"], "Not found.")
  def test_rate_delete_404(self):
    response = self.client.delete(self.url + str(2))
    self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    response = self.client.get(self.url)
    self.assertEqual(len(response.data), 3)
    self.assertEqual(response.data["id"], 1)
    self.assertEqual(response.data["value"], 999.0)