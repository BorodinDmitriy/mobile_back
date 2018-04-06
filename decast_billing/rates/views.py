# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.http import HttpResponse, Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Rate
from .serializers import RateSerializer

import logging

logger = logging.getLogger('django')

# Create your views here.
# /rate/?type=gas
class RateByType(APIView):
  def get(self, request):
    logger.info("Checking type..")
    if request.GET.get("type") is not None:
      logger.info("Getting rate..")
      rate = Rate.objects.get(type=request.GET.get("type"))
      logger.info("Trying to serialize rate object..")
      serializer = RateSerializer(rate)
      logger.info("Success.")
      return Response(serializer.data)
    logger.info("Error in type or rate with type does not exist.")
    return Response(status=status.HTTP_400_BAD_REQUEST)
  
# /rates/
class RateList(APIView):
  
  def get(self, request):
    logger.info("Getting list of rates..")
    rates = Rate.objects.all()
    logger.info("Trying to serialize list of rates..")
    serializer = RateSerializer(rates, many=True)
    logger.info("Success.")
    return Response(serializer.data)
  def post(self, request):
    logger.info("Trying to serialize rate object..")
    serializer = RateSerializer(data=request.data)
    if serializer.is_valid():
      logger.info("Saving..")
      serializer.save()
      logger.info("Success.")
      return Response(serializer.data,status=status.HTTP_201_CREATED)
    logger.info("Error in serializing rate object..")
    return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

# /rates/<id>/
class RateDetail(APIView):
  def get_object(self,id):
    try:
      logger.info("Trying to get rate by id..")
      return Rate.objects.get(id=id)
    except Rate.DoesNotExist:
      logger.info("Rate with this id does not exist.")
      raise Http404

  def get(self,request,id):
    logger.info("Getting snippet of rate..")
    snippet = self.get_object(id)
    logger.info("Trying to serialize rate object..")
    serializer = RateSerializer(snippet)
    logger.info("Success.")
    return Response(serializer.data)
  def put(self,request,id):
    try:
      logger.info("Getting snippet of rate..")
      snippet = self.get_object(id)
      snippet.id=id
      snippet.value=float(request.data["value"])
      logger.info("Updating..")
      snippet.save()
      logger.info("Success.")
      return Response(RateSerializer(snippet).data,status=status.HTTP_201_CREATED)
    except:
      logger.info("Error in updating rate.")
      return Response(status=status.HTTP_400_BAD_REQUEST)
  def delete(self,request,id):
    try:
      logger.info("Getting snippet of rate..")
      snippet = self.get_object(id)
      logger.info("Deleting..")
      snippet.delete()
      logger.info("Success.")
      return Response(status=status.HTTP_204_NO_CONTENT)
    except:
      logger.info("Error in deleting rate.")
      return Response(status=status.HTTP_400_BAD_REQUEST)