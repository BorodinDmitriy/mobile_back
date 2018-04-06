# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework.reverse import reverse
from django.test import TestCase,Client
from rest_framework import status
from rest_framework.test import APITestCase,APIClient



from devices.models import User,Device,Reading

# Create your tests here.


#class UserTests(unittest.TestCase):
#  client = Client()
  #def get_user_id(self):
    #url = reverse('user')
    #data = {'email' : 'Saboteuur@yandex.ru'}
    #response = client.get(url,data,format='json')
   # self.assertEqual(response.data, 5)
   # self.assertEqual(response.status_code, status.HTTP_200_OK)
 # def setUp(self):
  #  User.objects.create(id=1,login="demansen@yandex.ru")
  #def test_upper(self):
  #  url = '/user'
  #  data = {'email' : 'demansen@yandex.ru'}
 #   response = self.client.get(url,data,format='json')
  #  print(response)
 #   print(User.objects.all())
    #self.assertEqual(response.data, 5)
   # self.assertEqual(response.status_code, status.HTTP_200_OK)
   

class UserTestCase(APITestCase):
  def setUp(self):
    self.url="/user/"
    self.user={
      'id' : 9,
      'login' : "test@test.ru"
      }
    self.login={
      'login' : "test@test.ru"
      }
  def test_create(self):
    response = self.client.post(
            self.url,
            self.user
        )
    self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    user = User.objects.get(login=self.user['login'])
    self.assertEqual(user.id, self.user['id'])
    self.assertEqual(user.login, self.user['login'])
  def test_bad_create(self):
    del self.user['login']
    response = self.client.post(
            self.url,
            self.user
        )
    self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
  def test_good_get(self):
    response = self.client.post(
            self.url,
            self.user
        )
    self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    user={
      'email' : "test@test.ru"
      }
    response = self.client.get(self.url,user)
    
    user = User.objects.get(login=self.user["login"])
    self.assertEqual(response.status_code,status.HTTP_200_OK)
    self.assertEqual(user.id,response.data)
  def test_bad_get(self):
    response = self.client.post(
            self.url,
            self.user
        )
    self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    user={
      'email' : "test@tet.ru"
      }
    response = self.client.get(self.url,user)
    
    user = User.objects.get(login=self.user["login"])
    self.assertEqual(response.status_code,status.HTTP_404_NOT_FOUND)
  def test_getitem_good(self):
    response = self.client.post(
            self.url,
            self.user
        )
    self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    user = User.objects.get(login=self.user["login"])
    self.assertEqual(user.__getitem__("id"),9)
  def test_getitem_bad(self):
    response = self.client.post(
            self.url,
            self.user
        )
    self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    user = User.objects.get(login=self.user["login"])
    self.assertNotEqual(user.__getitem__("id"),8)
  def test_str_good(self):
    response = self.client.post(
            self.url,
            self.user
        )
    self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    user = User.objects.get(login=self.user["login"])
    self.assertEqual(user.__str__(),self.user["login"])
  def test_str_bad(self):
    response = self.client.post(
            self.url,
            self.user
        )
    self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    user = User.objects.get(login=self.user["login"])
    self.assertNotEqual(user.__str__(),self.user["login"] + '1')

class DeviceByUserIdTestCase(APITestCase):
  def setUp(self):
    self.user_url="/user/"
    self.user={
      'id' : 9,
      'login' : "test@test.ru"
      }
    self.url="/users/" + str(self.user['id']) + '/devices/'
    self.client.post(
            self.user_url,
            self.user
        )
    self.device={
      'personal_account' : '1',
      'serial_number' : '2'
      }
    self.new_device={
      'personal_account' : '3',
      'serial_number' : '4'
      }
  def test_create_device_for_user_good(self):
    response = self.client.post(
            self.url,
            self.device
        )
    self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    self.assertEqual(len(Device.objects.all()), 1)
    device = Device.objects.get(personal_account='1')
    self.assertEqual(self.device['serial_number'], '2')
  def test_create_device_for_user_bad(self):
    del self.device['personal_account'];
    response = self.client.post(
            "/users/8/devices/",
            self.device
        )
    self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
  def test_get_devices_for_user_good(self):
    response = self.client.post(
            self.url,
            self.device
        )
    self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    response = self.client.get(self.url)
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    self.assertEqual(len(response.data), len(Device.objects.all()))
  def test_get_devices_for_user_bad(self):
    response = self.client.post(
            self.url,
            self.device
        )
    self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    response = self.client.get(self.url + str(10))
    self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
  
class DeviceListTestCase(APITestCase):
  def setUp(self):
    self.user_url="/user/"
    self.user={
      'id' : 9,
      'login' : "test@test.ru"
      }
    self.url="/users/" + str(self.user['id']) + '/devices/'
    self.client.post(
            self.user_url,
            self.user
        )
    self.device={
      'personal_account' : '1',
      'serial_number' : '2'
      }
    self.new_device={
      'personal_account' : '3',
      'serial_number' : '4'
      }
    response = self.client.post(
            self.url,
            self.device
        )
    self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    self.devices_url = "/devices/"
  def test_get_device_list_good(self):
    response = self.client.get(self.devices_url)
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    self.assertEqual(len(response.data), len(Device.objects.all()))

class DeviceDetailTestCase(APITestCase):
  def setUp(self):
    self.user_url="/user/"
    self.user={
      'id' : 9,
      'login' : "test@test.ru"
      }
    self.client.post(
            self.user_url,
            self.user
        )
    self.device={
      'personal_account' : '1',
      'serial_number' : '2'
      }
    self.new_device={
      'personal_account' : "3",
      'serial_number' : "4"
      }
    self.uri="/users/" + str(self.user['id']) + '/devices/'
    self.url='/devices/1/'
    response = self.client.post(
            self.uri,
            self.device
        )
    self.assertEqual(response.status_code, status.HTTP_201_CREATED)
  def test_device_detail_get_good(self):
    response = self.client.get(self.url)
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    self.assertEqual(response.data["personal_account"], '1')
    self.assertEqual(response.data["serial_number"], '2')
  def test_device_detail_get_bad(self):
    response = self.client.get(self.url + str(2))
    self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
  def test_device_detail_put_good(self):
    response = self.client.put(self.url,self.new_device)
    self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    response = self.client.get(self.url)
    self.assertEqual(response.data["personal_account"], '3')
    self.assertEqual(response.data["serial_number"], '2')
  def test_device_detail_put_bad(self):
    del self.new_device["personal_account"]
    response = self.client.put(self.url,self.new_device)
    self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    response = self.client.get(self.url)
    self.assertEqual(response.data["personal_account"], '1')
    self.assertEqual(response.data["serial_number"], '2')
  def test_device_detail_delete_good(self):
    response = self.client.get(self.url)
    self.assertEqual(len(response.data), 5)
    response = self.client.delete(self.url)
    self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
    response = self.client.get(self.url)
    self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    self.assertEqual(response.data["detail"],'Not found.')
  def test_device_str_good(self):
    self.assertEqual(Device.objects.get(personal_account='1').__str__(),'1')
    
class DeviceReadingsTestCase(APITestCase):
  def setUp(self):
    self.user_url="/user/"
    self.user={
      'id' : 9,
      'login' : "test@test.ru"
      }
    self.client.post(
            self.user_url,
            self.user
        )
    self.device={
      'personal_account' : '1',
      'serial_number' : '2'
      }
    self.reading={
      "value":"123456"
      }
    self.uri="/users/" + str(self.user['id']) + '/devices/'
    self.url='/devices/1/readings/'
    response = self.client.post(
            self.uri,
            self.device
        )
    self.assertEqual(response.status_code, status.HTTP_201_CREATED)
  def test_create_reading_good(self):
    response = self.client.post(
            self.url,
            self.reading
        )
    self.assertEqual(response.status_code, status.HTTP_201_CREATED)
  def test_get_reading_good(self):
    response = self.client.post(
            self.url,
            self.reading
        )
    self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    response = self.client.get(self.url)
    self.assertEqual(len(response.data), 1)
  def test_reading_str_good(self):
    response = self.client.post(
            self.url,
            self.reading
        )
    self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    response = Reading.objects.get(id=1)
    self.assertEqual(response.__str__(), "123456")
  #def test_get_reading_params_good(self):
  #  response = self.client.post(
  #          self.url,
  #          self.reading
  #      )
  #  self.assertEqual(response.status_code, status.HTTP_201_CREATED)
  #  response = self.client.get(self.url,{"start_date":"2017-10-22T21:39:43.773734Z"})
  #  self.assertEqual(len(response.data), 1)