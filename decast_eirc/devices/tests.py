# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework.reverse import reverse
from django.test import TestCase,Client
from rest_framework import status
from rest_framework.test import APITestCase,APIClient



from devices.models import EIRCDevice

# Create your tests here.
class EIRCDeviceListTestCase(APITestCase):
  def setUp(self):
    self.url = "/eirc_devices/"
    self.eirc_device={
    "id": 1,
    "type": "water",
    "reading": "000001",
    "date": "2017-11-01T01:42:34.170963Z",
    "personal_account": "1234-1234-1234-1234",
    "serial_number": "000001"
    }
  def test_eirc_device_post_good(self):
    response = self.client.post(
            self.url,
            self.eirc_device
        )
    self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    self.assertEqual(len(EIRCDevice.objects.all()), 1)
    eirc_device = EIRCDevice.objects.get(type=self.eirc_device["type"])
    self.assertEqual(str(self.eirc_device['reading']), eirc_device.__str__())
  def test_eirc_device_post_bad(self):
    del self.eirc_device["id"]
    response = self.client.post(
            self.url,
            self.eirc_device
        )
    self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    self.assertEqual(len(EIRCDevice.objects.all()), 0)
  def test_eirc_device_get_good(self):
    response = self.client.post(
            self.url,
            self.eirc_device
        )
    self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    self.assertEqual(len(EIRCDevice.objects.all()), 1)
    response = self.client.get(self.url)
    self.assertEqual(len(response.data), 1)

class EIRCDeviceDetailTestCase(APITestCase):
  def setUp(self):
    self.eirc_devices_url = "/eirc_devices/"
    self.eirc_device={
    "id": 1,
    "type": "water",
    "reading": "000001",
    "date": "2017-11-01T01:42:34.170963Z",
    "personal_account": "1234-1234-1234-1234",
    "serial_number": "000001"
    }
    self.new_eirc_device={
    "id": 1,
    "type": "water",
    "reading": "000002",
    "date": "2017-11-01T01:42:34.170963Z",
    "personal_account": "1234-1234-1234-1235",
    "serial_number": "000002"
    }
    response = self.client.post(
            self.eirc_devices_url,
            self.eirc_device
        )
    self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    self.url="/eirc_devices/1/"
  def test_eirc_device_detail_get_good(self):
    response = self.client.get(self.url)
    self.assertEqual(len(response.data), 6)
    self.assertEqual(response.data["id"], 1)
    self.assertEqual(response.data["type"], "water")
    self.assertEqual(response.data["serial_number"], "000001")
  def test_eirc_device_detail_put_good(self):
    response = self.client.put(self.url,self.new_eirc_device)
    self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    response = self.client.get(self.url)
    self.assertEqual(len(response.data), 6)
    self.assertEqual(response.data["id"], 1)
    self.assertEqual(response.data["personal_account"], "1234-1234-1234-1235")
  def test_eirc_device_detail_put_bad(self):
    del self.new_eirc_device["personal_account"]
    response = self.client.put(self.url,self.new_eirc_device)
    self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    response = self.client.get(self.url)
    self.assertEqual(len(response.data), 6)
    self.assertEqual(response.data["id"], 1)
    self.assertEqual(response.data["type"], "water")
    self.assertEqual(response.data["personal_account"], "1234-1234-1234-1234")
  def test_eirc_device_detail_delete_good(self):
    response = self.client.delete(self.url)
    self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
    response = self.client.get(self.url)
    self.assertEqual(len(response.data), 1)
    self.assertEqual(response.data["detail"], "Not found.")
  def test_rate_delete_404(self):
    response = self.client.delete(self.url + str(2))
    self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    response = self.client.get(self.url)
    self.assertEqual(len(response.data), 6)
    self.assertEqual(response.data["id"], 1)
    self.assertEqual(response.data["type"], "water")
    self.assertEqual(response.data["serial_number"], "000001")
    
class EIRCChangeReadingTestCase(APITestCase):
  def setUp(self):
    self.eirc_devices_url = "/eirc_devices/"
    self.eirc_device={
    "id": 1,
    "type": "water",
    "reading": "000001",
    "date": "2017-11-01T01:42:34.170963Z",
    "personal_account": "1234-1234-1234-1234",
    "serial_number": "000001"
    }
    self.new_eirc_reading={
    "reading": "000002",
    }
  
    response = self.client.post(
            self.eirc_devices_url,
            self.eirc_device
        )
    self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    self.url="/eirc_devices/1/change_reading/"
  def test_eirc_change_reading_put_good(self):
    response = self.client.put(self.url,self.new_eirc_reading)
    self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    response = self.client.get('/eirc_devices/1/')
    self.assertEqual(len(response.data), 6)
    self.assertEqual(response.data["id"], 1)
    self.assertEqual(response.data["reading"], "000002")
  def test_eirc_change_reading_put_bad(self):
    del self.new_eirc_reading["reading"]
    response = self.client.put(self.url,self.new_eirc_reading)
    self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    response = self.client.get('/eirc_devices/1/')
    self.assertEqual(len(response.data), 6)
    self.assertEqual(response.data["id"], 1)
    self.assertEqual(response.data["type"], "water")
    self.assertEqual(response.data["serial_number"], "000001")