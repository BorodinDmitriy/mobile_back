# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.http import HttpResponse, Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import EIRCDevice
from .serializers import EIRCDeviceSerializer

import logging

logger = logging.getLogger('django')

# Create your views here.
# eirc_device/?personal_account=string
class EIRCDeviceByAccount(APIView):
  def get(self, request):
    logger.info("Checking personal account..")
    if request.GET.get("personal_account") is not None:
      eirc_device = EIRCDevice.objects.get(personal_account=request.GET.get("personal_account"))
      return Response(EIRCDeviceSerializer(eirc_device).data)
    logger.info("Incorrect personal account or it does not exist in request")
    return Response(status=status.HTTP_400_BAD_REQUEST)
  
# eirc_devices/
class EIRCDeviceList(APIView):
  
  def get(self, request):
    if request.user.is_authenticated():
      logger.info("Getting list of eirc devices..")
      eirc_devices = EIRCDevice.objects.all()
      logger.info("Trying to serialize list of eirc devices..")
      serializer = EIRCDeviceSerializer(eirc_devices, many=True)
      #if serializer.is_valid():
      logger.info("Success.")
      return Response(serializer.data)
    else:
      return Response(status=status.HTTP_401_UNAUTHORIZED)
  def post(self, request):
    logger.info("Trying to serialize eirc device object..")
    serializer = EIRCDeviceSerializer(data=request.data)
    if serializer.is_valid():
      logger.info("Saving...")
      serializer.save()
      logger.info("Success.")
      return Response(serializer.data,status=status.HTTP_201_CREATED)
    logger.info("Incorrect serialization of eirc device.")
    return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

# eirc_devices/<id>
class EIRCDeviceDetail(APIView):
  def get_object(self,id):
    try:
      logger.info("Getting eirc device by id..")
      return EIRCDevice.objects.get(id=id)
    except EIRCDevice.DoesNotExist:
      logger.info("404 - eirc device does not exist.")
      raise Http404

  def get(self,request,id):
    logger.info("Getting snippet of eirc devices..")
    snippet = self.get_object(id)
    logger.info("Trying to serialize snippet..")
    serializer = EIRCDeviceSerializer(snippet)
    logger.info("Success.")
    return Response(serializer.data)
  def put(self,request,id):
    try:
      logger.info("Getting snippet of eirc device..")
      snippet = self.get_object(id)
      print(snippet)
      snippet.id=id
      snippet.reading=snippet.reading
      snippet.personal_account=snippet.personal_account
      logger.info("Checking personal account..")
      if request.data["personal_account"] is not None:
	snippet.personal_account=request.data["personal_account"]
      #snippet.serial_number=snippet.serial_number
      #if request.data["serial_number"] is not None:
	#snippet.serial_number=request.data["serial_number"]
      logger.info("Updating..")
      snippet.save()
      logger.info("Success.")
      return Response(EIRCDeviceSerializer(snippet).data,status=status.HTTP_201_CREATED)
    except:
      logger.info("Error in updating eirc device..")
      return Response(status=status.HTTP_400_BAD_REQUEST)
  def delete(self,request,id):
    try:
      logger.info("Getting snippet of eirc device..")
      snippet = self.get_object(id)
      logger.info("Deleting..")
      snippet.delete()
      logger.info("Success..")
      return Response(status=status.HTTP_204_NO_CONTENT)
    except:
      logger.info("Error in deleting eirc device..")
      return Response(status=status.HTTP_400_BAD_REQUEST)

# eirc_devices/<id>/change_reading/
class EIRCChangeReading(APIView):
  def get_object(self,id):
    try:
      logger.info("Getting  eirc device by id..")
      return EIRCDevice.objects.get(id=id)
    except EIRCDevice.DoesNotExist:
      logger.info("Eirc device does not exist..")
      raise Http404

  def put(self,request,id):
    try:
      logger.info("Getting snippet of eirc device..")
      snippet = self.get_object(id)
      snippet.id=id
      snippet.reading=snippet.reading
      logger.info("Checking reading..")
      if request.data["reading"] is not None:
	snippet.reading=request.data["reading"]
      snippet.personal_account=snippet.personal_account
      snippet.serial_number=snippet.serial_number
      logger.info("Saving..")
      snippet.save()
      logger.info("Success.")
      return Response(EIRCDeviceSerializer(snippet).data,status=status.HTTP_201_CREATED)
    except:
      logger.info("Error in updatinf reading of eirc device..")
      return Response(status=status.HTTP_400_BAD_REQUEST)
